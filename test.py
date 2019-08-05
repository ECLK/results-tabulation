from sqlalchemy_schemadisplay import create_schema_graph
connection = "postgres://postgres:1234@localhost:5432/election"
graph = create_schema_graph(metadata=MetaData(connection), show_datatypes=False, show_indexes=False, rankdir='LR', concentrate=False)
graph.write_png('database_schema_diagram.png')