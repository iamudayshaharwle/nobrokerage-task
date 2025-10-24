# 🏡 NoBrokerage Property Chatbot

An intelligent **AI-powered property assistant** that answers real estate–related queries in natural language.  
The system uses **LangGraph**, **LangChain**, **Gemini 2.0 (Google Generative AI)**, and **Streamlit** to process user queries, generate SQL dynamically, execute them on a **SQLite database**, and respond conversationally.

---

## 📘 Features

✅ Converts CSV property data into a SQLite database  
✅ Generates SQL queries automatically from user questions  
✅ Provides friendly natural-language answers  
✅ Interactive Streamlit-based chat UI  
✅ Maintains multi-threaded chat sessions with memory  

---

## 🏗️ Project Architecture

data/
├── project.csv
├── ProjectAddress.csv
├── ProjectConfiguration.csv
└── ProjectConfigurationVariant.csv
database/
└── nobrokerage_properties.db
convert_db.py
nobrokerage_agent.py
app.py
frontend.py
.env
README.md



**Workflow Overview:**
1. **convert_db.py** → Merges and loads CSV data into a SQLite DB  
2. **nobrokerage_agent.py** → Uses LLM to generate and execute SQL  
3. **app.py** → Defines the LangGraph data flow  
4. **frontend.py** → Streamlit-based chat interface  



## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/iamudayshaharwale/nobrokerage-task.git
cd nobrokerage-chatbot

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # 

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Your Google Gemini API Key
Create a .env file in the root directory:
GOOGLE_API_KEY=your_gemini_api_key_here

5️⃣ Build the Database
Run: python convert_db.py
This generates: database/nobrokerage_properties.db

6️⃣ Run the Application
streamlit run frontend.py
Then open your browser at: http://localhost:8501


#### 💬 Example Queries
Query : Show me all 2BHK flats in pune under ₹1 Cr.
Response : I found four 2BHK flats in Pune, but all of them are priced above ₹1 Cr. The prices are ₹1.43 Cr, ₹1.89 Cr, ₹1.41 Cr, and ₹1.36 Cr.

Query : List all 2BHK properties with 3 balconies.
Response : Here's a 2BHK property with 3 balconies: Pristine02, located in Sai nagar, Pune. It is ready to move, unfurnished and available for sale at ₹12.00 Cr.

Query : show me most ready properties in pune under 2Cr.
Response : The property 'Pristine02' is a ready-to-move 2BHK property in Sai Nagar, Pune, priced at ₹12.00 Cr.

Query : show me 2BHK property under 2cr budget in wakad, pune.
Response : No properties available currently for the given information.

Query : hey , can you show me some properties near chembur under 3 cr.
Response : Yes, I can show you some properties near Chembur under 3 Cr. Here are some options: Ashwini(₹1.11 Cr,₹2.22 Cr), Gurukripa(₹1.30 Cr,₹1.50 Cr,₹2.90 Cr,₹2.90 Cr,₹2.60 Cr), Hari om(₹1.30 Cr,₹1.90 Cr,₹2.30 Cr), QUEENS PARK(₹1.09 Cr,₹1.87 Cr,₹1.72 Cr,₹2.39 Cr), Queens Glory(₹79.44 L), Queens Avenue(₹1.07 Cr,₹1.53 Cr,₹1.67 Cr).



##### 🧠 How Conversation Memory Works

The chatbot uses LangGraph memory nodes to remember context:

If a user first asks “Show me 2BHK flats in Pune”,
and then asks “What about under ₹1 Cr?”,
the system automatically connects both queries.
This enables multi-turn, context-aware property searching.
