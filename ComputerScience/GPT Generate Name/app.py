from flask import Flask, request, jsonify, send_from_directory
import openai

app = Flask(__name__)

# 设置OpenAI API密钥
openai.api_key = ""

@app.route('/get_name', methods=['POST'])
def get_name():
    data = request.json

    # 获取表单数据
    gender = data.get('gender')
    surname = data.get('surname')
    birth_date = data.get('birth_date')
    birth_time = data.get('birth_time')
    name_length = data.get('name_length')
    expectation = data.get('expectation')
    favorite_poem_or_name = data.get('favorite_poem_or_name')

    # 修改您的提示以获取更符合您期望的结果
    prompt = f"根据易经、命理、五行以及古诗等经典著作的相关理念，为一个{gender}孩子起名，姓{surname}，生日为{birth_date}，出生时间为{birth_time}，姓氏和名字共{name_length}个字。期望寓意：{expectation}。喜欢的诗句或名字：{favorite_poem_or_name}。请提供3个名字建议，建议包括姓氏和名字、属性:五行属性、给出名字中每个字吉祥的寓意、来源，来源从《诗经》、《周易》、《唐诗》、《宋诗》中找到的典故的出处，并输出对应的诗句。"
    
    # 调用OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,  # 增加 max_tokens 以获取更多信息
        n=1,  # 将n改为1，以便API在一个回答中返回3个名字建议
        stop=None,
        temperature=0.7,
    )


    name_suggestions = response.choices[0].text.strip()

    # 将名字建议及相关信息作为JSON响应返回
    return jsonify({"name_suggestions": name_suggestions})

@app.route('/<path:path>', methods=['GET'])
def serve_static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True)
