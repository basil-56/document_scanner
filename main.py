#pip install weasyprint
#pip install pygo
#pip install pangocffi
#pip install flask
#pip install python-doctr
#pip install tensorflow
#pip install tf2onnx
#pip install tensorflow-addons
#pip install rapidfuzz==2.15.1
#installed gtk 3 externally .exe
import os

os.environ['USE_TF']='1'
from flask import Flask,render_template,url_for,request
import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from werkzeug.utils import secure_filename
import re
import json






app = Flask(__name__)
model=ocr_predictor(pretrained=True)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_SSC',methods=['POST'])
def predict_SSC():
    matricmarksheet = request.files['SSC']  # Access file object using request.files
    filename_ssc = secure_filename(matricmarksheet.filename)
    filepath_ssc = os.path.join(app.root_path, 'Static', filename_ssc)
    matricmarksheet.save(filepath_ssc)
    
    class_ssc=''
    seatno_ssc=''
    percentage_ssc=''
    total_max_marks_ssc=850
    marks_obtained_ssc=''

    document_ssc = DocumentFile.from_pdf(filepath_ssc)
    result_ssc = model(document_ssc)

    s=str(result_ssc)
    delimiter1 = "value='"
    delimiter2 = "', confidence="

    # Pattern to match the text between the delimiters
    pattern = re.compile(re.escape(delimiter1) + "(.*?)" + re.escape(delimiter2))
    matches_ssc = re.findall(pattern, s)

    for index in range(0,len(matches_ssc)):
        if matches_ssc[index]=='ANNUAL':
            class_ssc=matches_ssc[index+1]

        elif matches_ssc[index]=='NUMBER':
            seatno_ssc=matches_ssc[index+1]

        elif matches_ssc[index]=='TOTAL:':
            temp=matches_ssc[index+1].split('/')
            marks_obtained_ssc=temp[0]
            total_max_marks_ssc=temp[1]

    try:
        percentage_ssc=round((int(marks_obtained_ssc)/int(total_max_marks_ssc)*100),2)
    except:
        percentage_ssc=''

    os.remove(filepath_ssc)

    dic_ssc_to_json={'class_ssc':class_ssc,
                 'seatno_ssc':seatno_ssc,
                'marks_obtained_ssc':marks_obtained_ssc,
                'total_max_marks_ssc':total_max_marks_ssc,
                'percentage_ssc':percentage_ssc}

    ssc_json_object = json.dumps(dic_ssc_to_json, indent = 4)

    return render_template('resultSSC.html', prediction_ssc=ssc_json_object)

@app.route('/predict_HSC',methods=['POST'])
def predict_HSC():
    intermarksheet = request.files['HSC']  # Access file object using request.files
    filename_hsc = secure_filename(intermarksheet.filename)
    filepath_hsc = os.path.join(app.root_path, 'Static', filename_hsc)
    intermarksheet.save(filepath_hsc)
    
    document_hsc = DocumentFile.from_pdf(filepath_hsc)
    result_hsc = model(document_hsc)
    hsc_str=str(result_hsc)

    delimiter1 = "value='"
    delimiter2 = "', confidence="

    # Pattern to match the text between the delimiters
    pattern = re.compile(re.escape(delimiter1) + "(.*?)" + re.escape(delimiter2))
    matches_hsc = re.findall(pattern, hsc_str)



    Hsc_Roll=0
    HSC_NO=[]
    hsc_class=''
    for a in range(0,len(matches_hsc)):
        if 'Date' in matches_hsc[a]:
            try:
                for b in range(1,6):
                    if len(matches_hsc[a+b])==4:
                        hsc_class=matches_hsc[a+b]
            except:
                c='' 
        if len(matches_hsc[a])==6:
            try:
                if str(int(matches_hsc[a]))==matches_hsc[a]:
                    Hsc_Roll=matches_hsc[a]
            except:
                c=1

        elif len(matches_hsc[a])==3:
            try:
                if str(int(matches_hsc[a]))==matches_hsc[a]:
                    HSC_NO.append(matches_hsc[a])
            except:
                c=1
    HSC_NO.sort()

    total_max_marks_hsc=1100
    hsc_Marks_obtained=HSC_NO[len(HSC_NO)-1]

    try:
        percentage_hsc=round((int(hsc_Marks_obtained)/int(total_max_marks_hsc)*100),2)
    except:
        percentage_hsc=''




    dict_to_json={
    'hsc_class':hsc_class,
    'Hsc_Roll':Hsc_Roll,
    'total_max_marks_hsc':total_max_marks_hsc,
    'hsc_Marks_obtained':hsc_Marks_obtained,
    'percentage_hsc':percentage_hsc



        
    }

    hsc_json_object = json.dumps(dict_to_json, indent = 4)

    os.remove(filepath_hsc)
    return render_template('resultHSC.html', prediction_hsc= hsc_json_object)

@app.route('/predict_NED',methods=['POST'])
def predict_NED():
    transcript = request.files['NED']  # Access file object using request.files
    filename_ned = secure_filename(transcript.filename)
    filepath_ned = os.path.join(app.root_path, 'Static', filename_ned)
    transcript.save(filepath_ned)

    document_ned = DocumentFile.from_pdf(filepath_ned)
    result_ned = model(document_ned)
    

    Class_NO= ''
    Seat_no=''
    Total_cgpa=4.0
    obtained_cgpa=''
    ned_trans=str(result_ned)
    delimiter1 = "value='"
    delimiter2 = "', confidence="

    # Pattern to match the text between the delimiters
    pattern = re.compile(re.escape(delimiter1) + "(.*?)" + re.escape(delimiter2))
    matches_ned = re.findall(pattern, ned_trans)

    print(matches_ned)

    Total_cgpa=4.0
    for a in range(0,len(matches_ned)):
        if matches_ned[a]=='No'and matches_ned[a-1]=='Seat':
            Seat_no=matches_ned[a+1]
        elif 'NED/' in matches_ned[a]:
        
            Class_NO= matches_ned[a][-4:]
    

        elif len(matches_ned[a])==5:
            temp=matches_ned[a]+'5'
            try:
                if str(float(temp))==temp:
                    obtained_cgpa=matches_ned[a]
            except:
                c=1

    



    dict_to_json_ned={
        
    'Class_ned':  Class_NO, 
    'Seat_ned':  Seat_no, 
    'Total_cgpa_ned':  Total_cgpa,
    'obtained cgpa':  obtained_cgpa


        
    }

    ned_json_object_ned = json.dumps(dict_to_json_ned, indent = 4) 
    print(ned_json_object_ned)    
    os.remove(filepath_ned)
    return render_template('resultNED.html', prediction_ned= ned_json_object_ned)

if __name__ == '__main__':
	app.run(debug=True)