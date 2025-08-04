import { useEffect } from "react";

export function useMcpClient(onCommand: (cmd: any) => void) {
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/mcp");
    ws.onmessage = (event) => {
      console.log("接受到消息")
      const cmd = JSON.parse(event.data);
      console.log(cmd);
      onCommand(cmd);
    };
    ws.onerror=(e)=>{
      console.log(e)
    };
    ws.onopen=()=>{
      console.log("连接成功")
    }
    return () => ws.close();
  }, []);
}