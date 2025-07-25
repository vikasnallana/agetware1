from flask import Blueprint, request, jsonify
from app import mysql
import math

main = Blueprint('main', __name__)

# --- 1. LEND ---
@main.route('/lend', methods=['POST'])
def lend():
    try:
        data = request.json
        customer_id = int(data['customer_id'])
        principal = float(data['loan_amount'])
        years = float(data['loan_period'])
        rate = float(data['rate_of_interest'])

        interest = (principal * years * rate) / 100
        total_amount = principal + interest
        emi = math.ceil(total_amount / (years * 12))

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO loans 
            (customer_id, principal, interest, total_amount, emi, loan_period, rate_of_interest) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (customer_id, principal, interest, total_amount, emi, years, rate))

        loan_id = cur.lastrowid

        cur.execute("INSERT INTO transactions (loan_id, type, amount) VALUES (%s, %s, %s)",
                    (loan_id, 'LEND', total_amount))

        mysql.connection.commit()
        cur.close()

        return jsonify({
            'loan_id': loan_id,
            'total_amount': total_amount,
            'monthly_emi': emi
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- 2. PAYMENT ---
@main.route('/payment', methods=['POST'])
def payment():
    try:
        data = request.json
        loan_id = int(data['loan_id'])
        amount = float(data['amount'])
        payment_type = data['type'].upper()  # 'EMI' or 'LUMPSUM'

        cur = mysql.connection.cursor()

        # Insert transaction
        cur.execute("INSERT INTO transactions (loan_id, type, amount) VALUES (%s, %s, %s)",
                    (loan_id, payment_type, amount))

        # Make sure 'amount_paid' column exists in loans table
        cur.execute("UPDATE loans SET amount_paid = amount_paid + %s WHERE loan_id = %s", (amount, loan_id))

        mysql.connection.commit()
        cur.close()

        return jsonify({
            'message': f'{payment_type} payment of ₹{amount} received for loan {loan_id}.'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@main.route('/ledger/<int:loan_id>', methods=['GET'])
def ledger(loan_id):
    cur = mysql.connection.cursor()

    # Get loan info
    cur.execute("SELECT total_amount, emi FROM loans WHERE loan_id = %s", (loan_id,))
    loan = cur.fetchone()

    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    total_amount, emi = loan

    # Get all transactions
    cur.execute("SELECT type, amount, transaction_date FROM transactions WHERE loan_id = %s ORDER BY transaction_date", (loan_id,))
    transactions = cur.fetchall()

    # Get total paid (excluding LEND)
    cur.execute("SELECT SUM(amount) FROM transactions WHERE loan_id = %s AND type != 'LEND'", (loan_id,))
    paid = cur.fetchone()[0] or 0

    balance = total_amount - paid
    emis_remaining = math.ceil(balance / emi) if emi > 0 else 0

    cur.close()

    return jsonify({
        'loan_id': loan_id,
        'total_amount': total_amount,
        'emi': emi,
        'amount_paid': paid,
        'balance': balance,
        'remaining_emis': emis_remaining,
        'transactions': [
            {
                'type': t[0],
                'amount': float(t[1]),
                'date': t[2].strftime('%Y-%m-%d %H:%M:%S')
            } for t in transactions
        ]
    })


@main.route('/overview/<int:customer_id>', methods=['GET'])
def account_overview(customer_id):
    cur = mysql.connection.cursor()

    # Get all loans for the customer
    cur.execute("""
        SELECT loan_id, principal, interest, total_amount, emi
        FROM loans
        WHERE customer_id = %s
    """, (customer_id,))
    loans = cur.fetchall()

    overview = []

    for loan in loans:
        loan_id, principal, interest, total_amount, emi = loan

        # Get total amount paid for this loan
        cur.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE loan_id = %s AND type != 'LEND'
        """, (loan_id,))
        paid = cur.fetchone()[0] or 0

        balance = total_amount - paid
        emis_left = math.ceil(balance / emi) if emi > 0 else 0

        overview.append({
            'loan_id': loan_id,
            'principal': principal,
            'interest': interest,
            'total_amount': total_amount,
            'emi': emi,
            'amount_paid': paid,
            'remaining_emis': emis_left
        })

    cur.close()

    return jsonify({
        'customer_id': customer_id,
        'loans': overview
    })
