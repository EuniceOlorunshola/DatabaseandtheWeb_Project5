# This module provides access to the variables used by the interpreter
import sys
#py2neo and its imported module
from py2neo import Graph
# define a function that uses the py2neo library to create a connection to the graph database and then takes a part name as input and returns the total cost of the part and its basic subparts using recursive
def compute_cost_of_part(part_name):
   # Read the schema file name from the command line argument
# if length of the argument in the command line is less then 3 it shows the print statement
    if len(sys.argv) < 3:
        print("Python program file and your username and password from the neo4j database connection should be included in the command line argument in the terminal Ex: python3 ComputePart.py neo4j(username) password(your own password) ")
    # Neo4j graph database connection
    # Displays the command line arguments by extracting all the elements that is contained in the input file
    g = Graph(auth=(sys.argv[1],sys.argv[2]))
    # This is when the function executes a cypher query to find the total cost of a part including the cost of any subparts. The reduce function is used to compute the product of x.qty for each x in r , the variable s is initilaized to 1 and is updated for element in r by multiplying it with x.qty and the price of the subpart.
    # The query uses the MATCH clause to find the node with the specified part name and the [r:subpart*0..] pattern to traverse any number of subpart relationship 
    # The return clause calculates the cost by multiplying the quantity of each subpart by its price and summing the results with round function to round  the result to 2 decimal places and then join the result with a dollar sign
    # multiplies the result of the reduce function by the price of the subpart sp to get the total cost of all subparts, the sum function then adds up the cost of all subparts to get the total cost of the part and has a tuple with two elements the total cost and rounding the decimal to 2 places
    query = f"MATCH (p:Part {{name: '{part_name}'}})-[r:subpart*0..]->(sp:Part {{type: 'basic'}}) WITH sp, r RETURN '$' + round(sum(reduce(s = 1, x in r | s * x.qty) * sp.price), 2)"
    # evaluate method is used to return a single result which is the total cost
    result = g.run(query).evaluate()
    return result
# define a function that uses the py2neo library to create a function to the graph database and then takes a part name as input and returns the name and cost of each subpart using recursive
def compute_subparts_of_part(part_name):
    g = Graph(auth=(sys.argv[1],sys.argv[2]))
    # Tis is when the function executes a Cypher query to return the name and total cost of each subpart. The reduce function is used to compute the product of x.qty for each x in r, the variable s is initialized to 1 and is updated for element in r by multiplying it with x.qty by each quantity
    # The query uses the MATCH clause to find the node with the specified part name and the [r:subpart*0..] pattern to traverse any number of subpart relationship
    # The return clause returns the names of each basic subpart and mutiply the names of each subparts by its quantity to get the cost 
    # uses ORDER BY to have the names of the subparts in ascending order
    query = f"MATCH (p:Part {{name: '{part_name}'}})-[r:subpart*0..]->(sp:Part {{type: 'basic'}}) WITH sp, r RETURN sp.name, sum(reduce(s = 1, x in r | s * x.qty)) as total_cost ORDER BY sp.name"
    # executes the Cypher query on the Neo4j graph database returned by g 
    # The result of this query is returned as a result object which can be used to iterate over the returned records
    # The result object will contain the subparts names , and the total cost of each subpart by the quantity
    result = g.run(query)
    # it returns both the name and cost of each subpart as a set of records
    return result
# The main part of the program is a loop that repeatedly prompts the user for input to choose between cost of part, subparts, or q for quit 
while True:
    print("(c) cost of part")
    print("(s) sub-parts")
    print("(q) quit\n")
    choice = input("What do you want to see: ")
    # If the user enter c , the program prompts for a part name and calls the function compute_cost_of_part to compute the cost of the part
    if choice == 'c':
        part_name = input("Enter part name: ")
        cost = compute_cost_of_part(part_name)
        if cost is None:
            print("Part not found")
        else:
            print(f"Cost of {part_name} is {cost}\n")
            # if the user enters s, the program prompts for a part name and calls the function compute_subparts_of_part to compute the suparts and there costs
    elif choice == 's':
        part_name = input("Enter part name: ")
        result = compute_subparts_of_part(part_name)
        if result is None:
            print("Part not found")
        else:
            print(f"Subparts of pname: {part_name}\n")
            for record in result:
                # record is a dictionary containing two keys the names of the subparts and total_cost which is the calculated total cost of the basic subpart
                # prints out the names of the subparts and its total cost as a integer, which is calculated by multiplying the quantity of each subpart by the price of the basic subpart
                # The f string is used to format the output so that it shows the subpart name and its total cost
                print(f"{record['sp.name']} {int(record['total_cost'])}\n")
    # if the user enters q the program exits the loop and terminates
    elif choice == 'q':
        break
    else:
      # prints an error message for invalid input
      print("Invalid input\n")