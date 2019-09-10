function setup(x,y) {
	var canvas = createCanvas(x, y);
	canvas.parent("graphic")
}

function draw(rows,cols,field) {

for(var j = 0; j < cols;j++)
	for(var i = 0; i < rows ; i++)
	{
		var y = (i * 15)+20;
		var x = (j * 15)+20;
		if(field[j][i] != "O")fill('red');
			else{
				fill('white');
			}
		stroke(0);
		ellipse(x, y,15,15);
	}


}


function CheckRowsCols(num){
	if(num > 0 && num <= 1000)return true;
	else{
		return false;
	}
}

function CheckDays(days){
	if(days > 0 && days <= 100)return true;
	else{
		return false;
	}
}


function  spoil(rows,cols,field,row1,col1,row2,col2){
	var newfield = new Array(cols)
	
	for (var i = 0; i < cols;i++)
		{
			newfield[i] = new Array(rows)
		}
	for(var i = 0; i < cols;i++) //t1 110 , t2  515
	{
		for(var j = 0; j < rows ; j++)
		{
			newfield[i][j] = "O";
		}
	}	

	newfield[col1][row1] = "X";
	newfield[col2][row2] = "X";

	for(var i = 0; i < cols ; i++)
		for(var j = 0; j < rows ; j++)
		{
			if (field[i][j] != "O")
			{
				i_copy = i + 1;
				if (i_copy >= 0 && i_copy < cols)
					newfield[i_copy][j] = "X";
				
				i_copy = i - 1
				if (i_copy >= 0 && i_copy < cols) 
					newfield[i_copy][j] = "X";

				j_copy = j + 1
				if (j_copy >= 0 && j_copy < rows)	
					newfield[i][j_copy] = "X";

				j_copy = j - 1
				if (j_copy >= 0 && j_copy < rows)
					newfield[i][j_copy] = "X";
			}
		}	

return newfield;	
}


function caller(){
	var rows = document.getElementById("rows").value;
	var cols = document.getElementById("cols").value;
	var days = document.getElementById("days").value;
	var coord1 = document.getElementById("coord1").value;
	var coord2 = document.getElementById("coord2").value;
	coord1 = coord1.split(",");
	coord2 = coord2.split(",");

	if((CheckRowsCols(rows) && CheckRowsCols(cols) && CheckDays(days)) != true) 
		alert("Enter rows & cols in interval 0 to 1000 AND days in interval 0 to 100")
	else{

		for(var i = 0;i < 2;i++)
		{
			coord1[i] = parseInt(coord1[i])-1;
			coord2[i] = parseInt(coord2[i])-1;
		}
		var width = rows * 15 + 60;
		var height = cols * 15 + 60;
		
		var field = new Array(cols);

		for(var i = 0; i < cols;i++)
		{
			field[i] = new Array(rows);			
		}

		for(var i = 0; i < cols;i++)
		{
			for(var j = 0;j< rows;j++)
			{
				field[i][j] = "O" ;
			}
		}
		// cols - rows 
		// col1 = [] , col2 = [] 
		// col1 = [row[]] , col2 = [row[]] row with the same lenght
		field[coord1[1]][coord1[0]] = "X";
		field[coord2[1]][coord2[0]] = "X";
		

		for(var i = 0; i < days;i++)
		{
			field = spoil(rows,cols,field,coord1[0],coord1[1],coord2[0],coord2[1])
		}

		setup(height,width);
		draw(rows,cols,field);

		var count = 0;
		for(var i = 0;i < cols;i++)
				{
					for(var j = 0;j < rows;j++)
					{
						if(field[i][j] == "O")count+=1;
					}
				}
		var content = "Output: " + count;
	    document.getElementById("output").innerHTML=content;


	}

	
}