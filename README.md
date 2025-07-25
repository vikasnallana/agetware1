
  <h1>💰 Bank Lending System</h1>
  <p>A simple RESTful API-based system built using <strong>Flask</strong> and <strong>MySQL</strong> to simulate a bank's loan management process.</p>
  <p>It supports lending money, accepting repayments (EMIs or lump sum), viewing transaction ledgers, and complete loan account overviews.</p>

  <div class="section">
    <h2>🧰 Features</h2>
    <ul>
      <li><strong>LEND</strong>: Give loans to customers without restrictions.</li>
      <li><strong>PAYMENT</strong>: Accept EMI or lump sum payments from borrowers.</li>
      <li><strong>LEDGER</strong>: View complete transaction history for a loan.</li>
      <li><strong>ACCOUNT OVERVIEW</strong>: Summary of all loans with interest, EMIs, balance, and more.</li>
    </ul>
  </div>

  <div class="section">
    <h2>🧮 Loan Calculations</h2>
    <ul>
      <li><strong>Interest (I)</strong> = Principal (P) × Years (N) × Rate (R)</li>
      <li><strong>Total Amount (A)</strong> = Principal (P) + Interest (I)</li>
      <li><strong>Monthly EMI</strong> = Total Amount (A) / (N × 12)</li>
    </ul>
  </div>

  <div class="section">
    <h2>🛠️ Tech Stack</h2>
    <ul>
      <li><strong>Backend</strong>: Python, Flask</li>
      <li><strong>Database</strong>: MySQL</li>
      <li><strong>API Testing</strong>: Postman</li>
    </ul>
  </div>

  <div class="section">
    <h2>📁 Folder Structure</h2>
    <pre>
bank-lending-system/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── config.py
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
    </pre>
  </div>

  <div class="section">
    <h2>🔐 Environment Variables</h2>
    <p>Create a <code>.env</code> file in the root directory:</p>
    <pre>
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=bank_system
    </pre>
  </div>

  <div class="section">
    <h2>🚀 Getting Started</h2>
    <pre>
# 1. Clone the repository
git clone https://github.com/yourusername/bank-lending-system.git
cd bank-lending-system

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup your .env file (see above)

# 5. Run the Flask server
python run.py
    </pre>
  </div>

  <div class="section">
    <h2>📬 Sample Postman Testing</h2>
    <h3>/lend</h3>
    <pre>
{
  "customer_id": 1,
  "loan_amount": 100000,
  "loan_period": 2,
  "interest_rate": 0.12
}
   
{
  "loan_id": 2,
  "amount": 5000,
  "type": "EMI"
}
    </pre>
  </div>

  <div class="section">
    <h2>👤 Author</h2>
    <p><strong>Name:</strong> Vikas</p>
    <p><strong>Project:</strong> Internship Assignment @ Agetware</p>
  </div>

</body>
</html>
