# To create an environment :
python -m venv venv
venv\Scripts\activate

# NOTE : If you get error like -- File D:\Development\AI\vscodews\langchain-proj\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at 
# https:/go.microsoft.com/fwlink/?LinkID=135170, run following command on power shell.
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# To install depencies for python modules you need for your project
pip install -r requirements.txt

# To run llama locally run following command :
ollama run mistral



# Index of programs
1. Basic RAG with LangChain and Ollama program.