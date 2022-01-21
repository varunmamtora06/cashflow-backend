## Local Setup
1. ```git clone https://github.com/varunmamtora06/cashflow-backend.git```
2. ```pip install -r requirements.txt```
3. ```cd cashflow_backend```
4. ```Make a .env file and specify following in it:```
```
SECRET_KEY=your-very-much-secret-key
ENV_DEBUG=True
```
5. ```cd cashflow_backend/main```
6. ```mkdir test_img```
7. ```cd cashflow_backend (i.e. cd ..)```
8. Download Tesseract-OCR file from [here](https://drive.google.com/file/d/1B0g05Tq5QBM7_Avixq_QQ9Emq-eTp0B3/view?usp=sharing)
9. Unzip that file to ```cashflow_backend``` i.e. in the project's root.
10. ```cd cashflow_backend```
11. ```python manage.py migrate``` 
12. ```python manage.py runserver``` 