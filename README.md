Here we assume that, MySQL, Kafka, Zookeeper, Kafdrop, Redis server has been configured. Let's move to next step:
#####################################MySQL-DB########################
USER: TodoList
Pass: Todo_List123

CREATE TABLE TodoList.todo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL
);

#####################################FastAPI########################
--install pip
py -m pip install --upgrade pip
py -m pip --version

--install vertual env
py -m pip install --user virtualenv

--Creating a virtual environment
py -m venv env

--to active venv
1.Open PowerShell
2.Run the following command: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser 
OR 
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser

--Activating a virtual environment
.\env\Scripts\activate

--Leaving the virtual environment
deactivate

--install fastAPI
pip install fastapi "uvicorn[standard]"

--import mongodb driver
pip install mysql-connector-python kafka-puthon redis 

--run fastAPI
uvicorn main:app --reload

--requirements check
pip freeze

#####################################ReactJS########################
--create react app
install nodeJS
npm install -g npm@9.6.5
npm install -g create-react-app

--go this directory
E:\Running\MyProject\FastApiReact
--runn to create
create-react-app react-fastapi

--need a extra package
cd E:\Running\MyProject\FastApiReact
npm install axios bootstrap

--after create app
cd react-fastapi
npm start
