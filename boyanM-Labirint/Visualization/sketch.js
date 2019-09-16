class Point{
	constructor(row,col,distance)
	{
		this.row = row;
		this.col = col;
		this.distance = distance;
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


function setup() {
	createCanvas(600, 600);


matrix = [
	[' ', ' ', ' ', ' ', ' ', ' ',' '],
	['*', '*', ' ', '*', '*', '*',' '],
	[' ', ' ', ' ', ' ', ' ', ' ',' '],
	[' ', '*', '*', '*', '*', '*', ' '],
	[' ', ' ', ' ', ' ', ' ',' ', 'e']
	]

	var ROWS = 5;
	var COLUMNS = 7;

	paths = [];
	route = [];

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

	var result = calculate(ROWS,COLUMNS,matrix,seen,paths);
	
	if(result == -1)
	{
		var content = "Output: " + "No route to the destination";
		document.getElementById("output").innerHTML=content;
	}
	else
	{	
		last = paths[paths.length - 1];
		for(var dist = result;dist >=0;dist--)
			for(var i = paths.length - 2;i >=0;i--)
			{
				if(paths[i].row + 1 == last.row || paths[i].row - 1 == last.row || paths[i].row == last.row)
					check1=true;
				else
					check1=false;
				if(paths[i].col + 1 == last.col || paths[i].col - 1 == last.col || paths[i].col == last.col)
					check2=true;
				else
					check2=false;
				if(paths[i].distance == dist && (check1 && check2) && paths[i].distance != last.distance)
				{
					last = paths[i];
					matrix[paths[i].row][paths[i].col] = "@";
				}
			}



		var content = "Output: " + result;
		document.getElementById("output").innerHTML=content;

	}	
	

}

function draw() {
	var ROWS = 5;
	var COLUMNS = 7;

	for(var row = 0; row < ROWS;row++)
	{
		for(var col = 0; col < COLUMNS;col++)
		{
			var y = (row * 30) + 20;
			var x = (col * 30) + 20;
			
			if(matrix[row][col] == 'e')fill('blue');
			else if(matrix[row][col] == "*")fill('black');
			else if(matrix[row][col] == "@")fill('green');
			else
			{
				fill('red');
			}
			stroke(0);
			rect(x, y,30,30);
		}
	}
}


function calculate(ROWS,COLUMNS,matrix){
	start = new Point(0,0,0);

	queue = new Queue();
	queue.enqueue(start);

	seen[0][0] = true;
	
	while(!queue.isEmpty())
	{
		position = queue.front();
		
		paths.push(position);

		var row = position.row;
		var col = position.col;
		var distance = position.distance;
		queue.dequeue();

		if(matrix[row][col] == "e")
		{
			return distance;
		}	

		//Move up
		if(row - 1 >= 0 && row-1 < ROWS && seen[row - 1][col] == false)
		{	
			distance +=1;
			position = new Point(row-1,col,distance);
			seen[row-1][col] =  true
			queue.enqueue(position);

		}

		//Move down
		if(row + 1 >= 0 && row + 1 < ROWS && seen[row + 1][col] == false)
		{
			distance +=1;
			position = new Point(row+1,col,distance);
			seen[row+1][col] =  true;
			queue.enqueue(position);
		}

		//Move right
		if(col + 1 >= 0 && col + 1 < COLUMNS && seen[row][col + 1] == false)
		{
			distance +=1;
			position = new Point(row,col+1,distance);
			seen[row][col+1] =  true;
			queue.enqueue(position);
		}

		//Move left
		if(col - 1 >= 0 && col - 1 < COLUMNS && seen[row][col - 1] == false)
		{
			distance +=1;
			position = new Point(row,col-1,distance);
			seen[row][col-1] =  true;
			queue.enqueue(position);
		}

	}
	return -1;

}
