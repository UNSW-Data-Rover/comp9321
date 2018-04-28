from flask import Flask,jsonify, request

app = Flask(__name__)

#database to hold data for orders and payment information
orders= []
payments=[]
order_id=0

#order object- input order number, coffee type, order cost and extra note
class Order:
	def __init__(self, oid, types, cost, additions, status):
		self.id= oid
		self.types = types
		self.cost = cost
		self.additions= additions
		self.status=status

#payment object- input order number to identify order and status to identify paid or not
class Payment:
	def __init__(self, id, amount, status, payment_type=None, card_no=None, card_expiry=None, card_name=None):
		self.id=id
		self.amount=amount
		self.status=status
		self.payment_type= payment_type
		self.card_no=card_no
		self.card_expiry=card_expiry
		self.card_name=card_name



@app.route("/orders", methods=['POST'])
def create_order():
	#check for required field
	if not request.args.get('types') or not request.args.get('cost'):
		return jsonify(error="missing required field: TYPES and COST"), 400

	else:
		types = request.args.get('types')

		#check cost for numeric input
		try:
			cost = float(request.args.get('cost'))
		except:
			return jsonify(error="Invalid input: COST input value should be numeric"), 400

		#check if additional optional data
		if request.args.get('additions'):
			extra = request.args.get('additions')
		else:
			extra= None


		global order_id
		order_id+=1
		
		orders.append(Order(order_id, types, cost, extra, "unpaid"))
		payments.append(Payment(order_id, cost, "unpaid"))

		links=[{

			"href": "/orders",
			"rel": "self"},
			{
			"href":"/payments/"+ str(order_id),
			"rel":"nextPage"}]

		return jsonify(id=order_id, cost=cost, links=links), 201


@app.route("/orders/<number>", methods=['PUT'])
def update_order(number):
	number=int(number)

	for order in orders:
		if order.id == number:
			if order.status=="unpaid":
				if request.args.get('types'):
					order.types = request.args.get('types')

				if request.args.get('cost'):
					try:
						float(request.args.get('cost'))
						order.cost = request.args.get('cost')
					except:
						return jsonify(error="Invalid input: COST input value should be numeric"), 400

				if request.args.get('additions'):	
					order.additions = request.args.get('additions')
				return jsonify(order.__dict__), 200

			elif order.status=="paid":
				if request.args.get('status')=="prepared":
					order.status=request.args.get('status')
					return jsonify(order.__dict__), 200
				else:
					return jsonify(error="Invalid operation: Order cannot be changed"), 409

			else:
				return jsonify(error="Invalid operation: Order cannot be changed"), 409

	return jsonify(number=False), 404


@app.route("/orders/<number>", methods=['GET'])
def get_order(number):
	try:
		number=int(number)
	except:
		return jsonify(error="Invalid input: <number> must be numeric"), 400
	for order in orders:
		number=int(number)
		if order.id == number:
			return jsonify(order.__dict__), 200
	return jsonify(number=False), 404




@app.route("/orders/<number>", methods=['DELETE'])
def delete_order(number):
	try:
		number=int(number)
	except:
		return jsonify(error="Invalid input: <number> must be numeric"), 400

	for order in orders:
		if order.id == number:
			if order.status == "unpaid":
				order.status="cancelled"
				return jsonify(delete= number), 200
				
			else:
				return jsonify(error="Conflict: order cannot be cancelled"), 409
	return jsonify(number=False), 404

@app.route("/orderlist/<status>", methods=['GET'])
def get_statuslist(status):
	statuss=["paid", "unpaid", "cancelled", "prepared"]
	if status not in statuss:
		return jsonify(error="Invalid input: status must be 'paid', 'unpaid', 'cancelled' or 'prepared'"), 400
	status_list=[]
	for order in orders:
		if order.status== status:
			status_list.append(order)
	return jsonify([st.__dict__ for st in status_list]), 200

@app.route("/open_orders", methods=['GET'])
def get_orderlist():
	order_list=[]
	for order in orders:
		if order.status!="prepared" and order.status!="cancelled":
			order_list.append(order)
	return jsonify([st.__dict__ for st in order_list]), 200


@app.route("/payments/<number>", methods=['GET'])
def get_payment(number):
	number=int(number)
	for payment in payments:
		if payment.id==number:
			return jsonify(payment.__dict__), 200
	return jsonify(number=False), 404


@app.route("/payments/<number>", methods=['PUT'])
def create_payment(number):
	number=int(number)

	#check validity of input
	if not request.args.get("payment_type"):
		return jsonify(error="Missing required field: PAYMENT_TYPE"), 400

	payment_type=request.args.get("payment_type")
	if payment_type=="card":
		#additional fields are required if paid by card
		if not request.args.get("card_name") or not request.args.get("card_no") or not request.args.get("card_expiry"):
			return jsonify(error="Missing required field: CARD_NO or CARD_NAME, CARD_EXPIRY"), 400

		try:
			card_no=int(request.args.get("card_no"))
		except:
			return jsonify(error="Invalid input: Card_NO should be of 12 digits number"), 400

		card_check=list(str(card_no))
		if len(card_check)!=12:
			return jsonify(error="Invalid input: Card_NO should be of 12 digits number"), 400

		card_name= request.args.get("card_name")
		card_expiry= request.args.get("card_expiry")

	elif payment_type=="cash":
		card_name=None
		card_no=None
		card_expiry=None
	else:
		return jsonify(error="Invalid input: 'CARD' or 'CASH' in PAYMENT_TYPE"), 400



	for payment in payments:
		if payment.id==number:
			if payment.status=="paid":
				return jsonify(error="Order ID already PAID"), 400
			payment.status="paid"
			payment.payment_type=payment_type
			payment.card_no=card_no
			payment.card_expiry=card_expiry 
			payment.card_name=card_name
			for order in orders:
				if order.id== number:
					order.status="paid"
			return jsonify(payment.__dict__), 200
	return jsonify(number=False), 404



if __name__ == "__main__":
	app.run()