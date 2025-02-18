import json
from pymilvus import connections, utility, Collection

def export_milvus_data(host='localhost', port='19530', export_dir='./milvus_data', exclude_fields=None):
    """
    导出Milvus数据（排除指定字段）
    :param exclude_fields: 要排除的字段列表，默认排除content_vector
    """
    exclude_fields = exclude_fields or ["content_vector"]
    
    try:
        connections.connect(host=host, port=port, timeout=10)
        print(f"Connected to Milvus: {host}:{port}")

        import os
        os.makedirs(export_dir, exist_ok=True)

        for collection_name in utility.list_collections():
            print(f"\nProcessing: {collection_name}")
            
            col = Collection(collection_name)

            # 动态获取需要导出的字段
            valid_fields = [
                field.name 
                for field in col.schema.fields 
                if field.name not in exclude_fields
            ]
            print(f"Exporting fields: {valid_fields}")

            # 分页参数配置
            query_params = {
                "expr": "",
                "output_fields": valid_fields,  # 使用过滤后的字段列表
                "limit": 10000,
                "offset": 0
            }

            total = 0
            all_data = []
            while True:
                try:
                    results = col.query(**query_params)
                except Exception as e:
                    print(f"Query error: {str(e)}")
                    break

                if not results:
                    break
                
                # 处理特殊数据类型
                for item in results:
                    processed = {}
                    for k, v in item.items():
                        if hasattr(v, 'tolist'):  # 处理向量等numpy类型
                            processed[k] = v.tolist()
                        elif isinstance(v, bytes):  # 处理二进制数据
                            processed[k] = f"BINARY_DATA({len(v)} bytes)"
                        else:
                            processed[k] = v
                    all_data.append(processed)

                total += len(results)
                query_params["offset"] += len(results)
                print(f"Progress: {total} entities")

            # 保存数据
            if all_data:
                filename = f"{export_dir}/{collection_name}.json"
                with open(filename, 'w') as f:
                    json.dump(all_data, f, default=str, indent=2)
                print(f"Excluded fields: {exclude_fields}")
                print(f"Exported {len(all_data)} entities to {filename}")
            else:
                print("No data found")

    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        connections.disconnect()

if __name__ == "__main__":
    # 调用示例：排除content_vector和optional_bin_field
    export_milvus_data(
        host="localhost",
        port="19530",
        export_dir="./milvus_backup",
        exclude_fields=["content_vector", "optional_bin_field"]  # 可配置多个排除字段
    )
