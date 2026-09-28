import sys, json
from client import AgentWebStealthScraperDistiller

def handle_mcp():
    distiller = AgentWebStealthScraperDistiller()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(distiller.run_benchmark_web_distiller(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-agent-web-stealth-scraper-distiller-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "distill_html_to_markdown", "description": "Convert raw HTML into clean dense markdown.", "inputSchema": {"type": "object", "properties": {"html_content": {"type": "string"}}}},
                    {"name": "extract_page_metadata", "description": "Extract canonical title and metadata from HTML.", "inputSchema": {"type": "object", "properties": {"html_content": {"type": "string"}}}},
                    {"name": "run_benchmark_web_distiller", "description": "Benchmark web page parsing speed.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "distill_html_to_markdown":
                    res = distiller.distill_html_to_markdown(args.get("html_content", ""))
                elif tname == "extract_page_metadata":
                    res = distiller.extract_page_metadata(args.get("html_content", ""))
                else:
                    res = distiller.run_benchmark_web_distiller()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
