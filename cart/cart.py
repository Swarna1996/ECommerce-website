from store.models import Product,Profile

class Cart():
    def __init__(self,request):
        self.session = request.session
        self.request = request

        #Get the current session key if it exists
        #Every Django request has a session object, which behaves like a Python dictionary.
        cart = self.session.get('session_key')

        #if the user is new, no session key! create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Now, self.cart is accessible in other methods of this Cart class.
        self.cart = cart

    
    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty =str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))



    def cart_total(self):
        # Get products keys
        product_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantites
        quantities = self.cart
        total = 0
        # {'4':3,'2':5,'3':1,'1':3} self.cart return this type of dict {'product_id':quantity}
        for key, value in quantities.items():
             #convert string into int
             key = int(key)
             for product in products:
                  if product.id == key:
                        if product.is_sale:
                            total+=(product.sale_price*value)
                        else:
                            total+=(product.price*value)

        return total
                    
                  


    #To count how many items in out cart
    def __len__(self):
	    return len(self.cart)
    
    
    def get_prods(self):
         #Get ids from cart
         product_ids = self.cart.keys()
         #Use ids to lookup products in database model
         products = Product.objects.filter(id__in=product_ids) 
         #"__in" A lookup expression provided by Django ORM, which means “check if the field value is in a given list/iterable.”

         return products
    
    def get_quants(self):
         quantities = self.cart
         return quantities
    
    def update(self, product, quantity):
         product_id = str(product)
         product_qty = int(quantity)
         
         ourcart = self.cart
         ourcart[product_id] = product_qty

         self.session.modified = True

         thing = self.cart
         return thing
    
    def delete(self,product):
         
        product_id = str(product)
        #delete from dictionary
        if product_id in self.cart:
             del self.cart[product_id]

        self.session.modified = True
         
         
         

