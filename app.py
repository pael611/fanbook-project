from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://rafael:1234@cluster0.7se4f46.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    sample_receive = request.form['bucket_post']
    count = db.bucket.count_documents({})
    num = count + 1
    print(sample_receive)
    data = {
        'bucket': sample_receive,
        'num': num,
        'done':0
        
    }
    db.bucket.insert_one(data)
    
    return jsonify({'msg': 'POST data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    sample_parameter= request.form['sample_give']
    db.bucket.update_one({'num':int(sample_parameter)},
                          {'$set':{'done':1}})
    return jsonify({'msg': 'SUCCESS UPDATE!'})

@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    sample_parameter= request.form['sample_give']
    db.bucket.delete_one({'num':int(sample_parameter)})
    return jsonify({'msg': 'SUCCESS delete!'})



@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)