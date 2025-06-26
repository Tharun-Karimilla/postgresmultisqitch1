import os
from collections import defaultdict

def parse_dependencies():
    graph = defaultdict(list)
    all_schemas = []

    for schema in os.listdir():
        if os.path.isdir(schema) and schema.startswith("schema"):
            all_schemas.append(schema)
            plan_file = os.path.join(schema, "sqitch.plan")
            if not os.path.exists(plan_file):
                continue
            with open(plan_file) as f:
                for line in f:
                    if ":" in line and "[" in line:
                        start = line.find("[") + 1
                        end = line.find("]")
                        dep = line[start:end]
                        dep_schema = dep.split(":")[0]
                        if dep_schema != schema:
                            graph[schema].append(dep_schema)

    return topological_sort(graph, all_schemas)

def topological_sort(graph, nodes):
    visited, result, temp = set(), [], set()
    def visit(n):
        if n in temp:
            raise Exception("Cycle detected")
        if n not in visited:
            temp.add(n)
            for m in graph[n]:
                visit(m)
            temp.remove(n)
            visited.add(n)
            result.append(n)
    for node in nodes:
        visit(node)
    return result[::-1]

if __name__ == "__main__":
    order = parse_dependencies()
    print("::set-output name=deployment_order::" + str(order))
