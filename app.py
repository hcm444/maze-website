from flask import Flask, render_template, request
import base64
import maze

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', maze_image='maze.png')

@app.route('/update', methods=['POST'])
def update():
    try:
        image_data = request.form['image_data']
        save_path = 'static/saved_image.png'
        save_path_new = 'static/maze.png'

        with open(save_path, 'wb') as f:
            f.write(base64.b64decode(image_data))

        maze.update_maze_image(save_path, save_path_new)

        return "Image updated."
    except Exception as e:
        return f"Error updating image: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
