```
conda create -n SEI202411 python=3.11 -y
conda activate SEI202411
```

pip install -r requirements.txt

username = "robin1"
password = "ASDqwe123##1"
dsn = "207.211.167.18:1521/robin_pdb.sub05270741160.vcnrobin.oraclevcn.com"
#############################
qa:
1.embedding model
2.

# 数据生成

帮我生成班级表，班级人员表，考试表，考试成绩表的表结构，考试成绩表包含语文，数学，英语，数据库是sqlite，请帮我生成表结构。
班级有5个班级，每个班级有30个学生，请帮我生成2023年期末考试成绩和2024年期末考试成绩的数据。

学生表的表结构如下，班级有5个班级，每个班级有30个学生，请帮我生成这个表的数据。

CREATE TABLE student_table (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 学生ID
    student_name TEXT NOT NULL, -- 学生姓名
    class_id INTEGER NOT NULL, -- 所属班级ID
    FOREIGN KEY (class_id) REFERENCES class_table(class_id)
);

############################
streamlit run .\main_streamlit.py
streamlit run .\main_streamlit_full.py

## questions

```
現在の収益は、どんな状況
組織ごとの収益を教えて


FUSION、教えて
現在の収益は、どんな状況

組織ごとの収益を教えて,棒グラフにして

このデータを棒グラフにして

この折れ線グラフにしてみて

最初の棒グラフを低い順に並べて

このグラフをパワーポイントファイルにして
```

```easycode
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)


    return vn.is_sql_valid(sql=sql)


    return vn.run_sql(sql=sql)


    return vn.should_generate_chart(df=df)


    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code



    return vn.get_plotly_figure(plotly_code=code, df=df)


    return vn.generate_summary(question=question, df=df)
```

def generate_ppt(message, history):
    # Create a PPT file
    prs = pptx.Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    title.text = "Example PPT File"

    # Save the PPT file to a file object
    from io import BytesIO
    file_object = BytesIO()
    prs.save(file_object)
    file_object.seek(0)
    # save this file object to a file
    # file_object.name = "example.pptx"
    with open('example.pptx', 'wb') as f:
        # Write the BytesIO object to the file
        f.write(file_object.getvalue())
    
    # Return a dictionary with the PPT file as the 'content' value
    # return [{"role": "assistant", "content": gr.File("example.pptx")}, {"role": "assistant", "content": "wwwwww"}]
    return [{'role': 'assistant', 'content': 'This is the first message'},
            {'role': 'assistant', 'content': 'This is the second message'}]

def plot_graph(message, history):
    # Generate the graph
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.title("Example Graph")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")

    # Save the graph to a file
    plt.savefig("graph.png")
    
    # Display the graph in the chat interface
    return {"role": "assistant", "content": gr.Image("graph.png")}

import plotly.io as pio

# 假设 `self` 是一个图表对象，如 plotly.graph_objects.Figure

# def save_plot_to_file(self, file_path, *args, **kwargs):

# # 将图表转换为图像格式（例如 PNG）

# image_bytes = pio.to_image(self, *args, **kwargs)

# 

# # 将字节写入本地文件

# with open(file_path, 'wb') as f:

# f.write(image_bytes)

# 

# 

# # 示例调用方法

# # self 是要保存的图表对象（如 Figure）

# # 'output.png' 是保存的文件路径

# save_plot_to_file(self, 'output.png', format='png')  # format 可选 png, jpg, svg 等
