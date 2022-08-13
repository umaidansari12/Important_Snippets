npm run build
to create an optimized production build - static assest that you will deploy in prod

npm i -g serve
install serve 

serve -s build -p 8000
serve build folder on port 8000

Lecture Notes: This will be useful for revising what we learnt after the video. If you feel this is helpful, I'll create for the reset of the video too. Paste it in a code editor for better readability.
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------   
01:46 - Var, Let, Const
    * Var: the variable defined is visible in the entire function.
    * Let: the variable defined is visible only in the block it is defined in.
    * Const: makes the variable a constant
    * Use const over let and let over var wherever possible
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------        
05:40 - Objects
   * const person = {
   		"name": "Mosh",
   		walk() {},
   		talk() {}
   	}
   	Above is an object with 1 property and 2 methods.
   	Another way defining a method member in an object is:
   	walk: function() {} //not recommended
   	* Invoking method of an object: person.walk()
   	* Accessing property of object
   		** When the property is known in advance: person["name"]
   		** When the property is not known in advance: person[variable.value] //variable.value == "name"
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------  
08:27 - The this Keyword
	* const person = {
   		"name": "Mosh",
   		walk() {
   			console.log(this)
   		}
   	}
	this in the function walk always refers to the object which invoked it, and by default by the global object (window)
	person.walk() => the person object is printed on console, since the function walk is invoked by person object and thus "this" represent it here.
	const walk1 = person.walk //not calling the function, only assiging variable walk1 the function walk
	walk1()	=> undefined is printed since the default object is the global object and "this"  represents it here.
	If strict mode is not enabled, it will return window object instead of undefine
	* All functions in JS are object which have member functions like bind.
	const walk1 = person.walk.bind(person)
	here bind function on walk sets the "this" in it as the reference to the object that is passed to it.
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------  
13:57 - Arrow Functions 
	* Different ways of declaring functions:
		** const square = function(number) { return number*number}
		** const square = (number) => {return number*number}
		** const square = number => return number*number
		** const 2square = () => return 4 // () is required when the function has no input parameters

