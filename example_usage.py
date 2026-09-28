from client import AgentWebStealthScraperDistiller
import json

def test():
    d = AgentWebStealthScraperDistiller()
    print("=== Testing Agent Web Stealth Scraper & Distiller ===")
    res = d.run_benchmark_web_distiller()
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    test()
