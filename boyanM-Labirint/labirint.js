function setup() {
	createCanvas(600, 600);
}

function draw() {
	matrix = [
	[' ', ' ', ' ', '*', ' ', ' ',' '],
	[' ', ' ', ' ', '*', '*', '*',' '],
	[' ', ' ', ' ', ' ', ' ', ' ',' '],
	['*', '*', '*', ' ', '', ' ', ' '],
	[' ', ' ', ' ', ' ', ' ',' ', 'e']
	]

	var ROWS = 5;
	var COLUMNS = 7;

	var result = calculate(ROWS,COLUMNS,matrix);
	for(var row = 0; row < ROWS;row++)
	{
		for(var col = 0; col < COLUMNS;col++)
		{
			var y = (row * 30) + 20;
			var x = (col * 30) + 20;
			
			if(matrix[row][col] == 'e')fill('blue');
			else if(matrix[row][col] == "*")fill('black')
			else
			{
				fill('red');
			}
			stroke(0);
			rect(x, y,30,30);
		}
	}
}



class Point{
	constructor(row,col)
	{
		this.row = row;
		this.col = col;
		this.distance = 0;
	}
}

class Queue{
	constructor()
	{
		this.data = [];
	}

	enqueue(newElement)
	{
		this.data.push(newElement);
	}

	dequeue()
	{
		if(this.isEmpty())return "Underflow";
		else
		{
			this.data.shift();
		}
	}

	front()
	{
		if(this.isEmpty())return "Empty Queue";
		else
		{
			return this.data[0];
		}
		
	}

	isEmpty()
	{
		return this.data.length == 0 // <==> if length is equal to 0 return true else false
	}

	printQueue() //return Queue as a String
	{
		var string = ""
		for(var i = 0; i < this.data.length;i++)
		{
			string += this.data[i]+",";
		}
		return string
	}

}
function calculate(ROWS,COLUMNS,matrix){

	seen = new Array(ROWS)
	for(var row = 0; row < COLUMNS;row++)
	{
		seen[row] = new Array(COLUMNS)
	}

	for(var row = 0; row < ROWS;row++)
	{
		for(var col = 0; col < COLUMNS;col++)
		{
			if(matrix[row][col] == "*")seen[row][col] = true;
			else
			{
				seen[row][col] = false;
			}
		}
	}

	start = new Point(0,0);

	queue = new Queue();
	queue.enqueue(start);

	position = start;
	while(!queue.isEmpty())
	{
		var row = position.row;
		var col = position.col;
		var distance = position.distance;
		queue.dequeue();
		if(matrix[row][col] == "e")
			return distance;

		//Move down
		if(row - 1 >= 0 && row-1 < ROWS && seen[row - 1][col] == false)
		{
			position.row = row -1;
			position.col = col;
			position.distance = distance + 1;
			seen[row-1][col] =  true
			queue.enqueue(position);
			
		}

		//Move up
		if(row + 1 >= 0 && row + 1 < ROWS && seen[row + 1][col] == false)
		{
			position.row = row + 1;
			position.col = col;
			print.distance = distance + 1;
			seen[row+1][col] =  true;
			queue.enqueue(position);
		}

		//Move right
		if(col + 1 >= 0 && col + 1 < COLUMNS && seen[row][col + 1] == false)
		{
			position.row = row;
			position.col = col + 1;
			print.distance = distance + 1;
			seen[row][col+1] =  true;
			queue.enqueue(position);
		}

		//Move left
				//Move down
		if(col - 1 >= 0 && col - 1 < COLUMNS && seen[row][col - 1] == false)
		{
			position.row = row;
			position.col = col - 1;
			print.distance = distance + 1;
			seen[row][col-1] =  true;
			queue.enqueue(position);
		}
		position = queue.front()

	}
	return "No path to the destination !"

}
