from flask import Flask,request,jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

cursos=[
    {'id':1,'codigo':'CS101','nombre':'lenguaje'},
    {'id':2,'codigo':'CS102','nombre':'matematicas'}
]

@app.route('/cursos',methods=['GET'])
def listar_cursos():
    return jsonify(cursos)

@app.route('/cursos/<int:id>',methods=['GET'])
def obtener_cursos(id):
    curso=next((c for c in cursos if c['id']==id),None)
    if curso:
        return jsonify(curso)
    return jsonify({'error':'curso no encontrado'}),404

@app.route('/cursos',methods=['POST'])
def crear_curso():
    data=request.get_json()
    nuevo={'id':len(cursos)+1,'codigo':data['codigo'],'nombre':data['nombre']}
    cursos.append(nuevo)
    return jsonify(nuevo),201

if __name__=='__main__':
    app.run(debug=True)