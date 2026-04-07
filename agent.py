from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

# Tạo thư mục lưu trữ nếu chưa có
os.makedirs("logs", exist_ok=True)
os.makedirs("traces", exist_ok=True)

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Inject System Prompt vào đầu danh sách nếu chưa có
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    
    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print("Trả lời trực tiếp")
        
    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)

# Thêm các nút (Nodes)
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Hoàn thiện các cạnh nối (Edges) - TODO trong ảnh
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent") # Sau khi chạy tool thì quay lại agent để suy nghĩ tiếp

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch Thông minh")
    print("      Gõ 'quit' để thoát")
    print("=" * 60)
    
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Tạm biệt!")
            break
            
        print("\nTravelBuddy đang suy nghĩ...")
        
        # Để lưu lại toàn bộ diễn biến (traces) và đàm thoại (logs)
        current_steps = []
        final_answer = ""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            # Sử dụng stream để bắt từng bước thực thi của Graph
            for chunk in graph.stream({"messages": [("human", user_input)]}):
                # Chunk chứa thông tin về nút vừa chạy (vd: node 'agent' hoặc 'tools')
                current_steps.append(chunk)
                
                for node, values in chunk.items():
                    if node == "agent":
                        last_msg = values["messages"][-1]
                        final_answer = last_msg.content
            
            # Lấy kết quả cuối cùng để hiển thị
            print(f"\nTravelBuddy: {final_answer}")

            # --- LƯU TRACE (Suy nghĩ chi tiết) ---
            trace_file = f"traces/trace_{timestamp}.json"
            with open(trace_file, "w", encoding="utf-8") as f:
                # Chuyển đổi các đối tượng message sang dict để lưu JSON
                serializable_steps = [str(step) for step in current_steps]
                json.dump(serializable_steps, f, ensure_ascii=False, indent=2)

            # --- LƯU LOG (Cuộc hội thoại) ---
            log_file = f"logs/chat_{datetime.now().strftime('%Y-%m-%d')}.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] Bạn: {user_input}\n")
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] TravelBuddy: {final_answer}\n")
                f.write("-" * 30 + "\n")
        except Exception as e:
            # CƠ CHẾ FALLBACK: Trả lời thân thiện khi hệ thống/API có lỗi
            error_msg = "Xin lỗi bạn, hệ thống của mình đang gặp một chút trục trặc kỹ thuật. Bạn vui lòng thử lại sau giây lát nhé!"
            print(f"\nTravelBuddy: {error_msg}")
            
            # Lưu log lỗi để debug
            with open(f"logs/error_{datetime.now().strftime('%Y-%m-%d')}.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] Lỗi: {str(e)}\n")
