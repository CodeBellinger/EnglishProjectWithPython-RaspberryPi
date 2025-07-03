from ulib import display, fancy
import time

display.fill((0,0,0))
r = (196,196,196)
int pos
int posdisplacement = (pos-1)*4
Eins = {											(5,2+posdisplacement):r;
							(6,1+posdisplacement):r;(6,2+posdisplacement):r;	
	(7,0+posdisplacement):r;						(7,2+posdisplacement):r;	
													(8,2+posdisplacement):r;		
													(9,2+posdisplacement):r;	
													(10,2+posdisplacement):r;
			}
Zwei = {					(5,1+posdisplacement):r;	
	(6,0+posdisplacement):r;(6,1+posdisplacement):r;(6,2+posdisplacement):r;			
	(7,0+posdisplacement):r;						(7,2+posdisplacement):r;	
													(8,2+posdisplacement):r;	
							(9,1+posdisplacement):r;	
	(10,0+posdisplacement):r;(10,1+posdisplacement):r;(10,2+posdisplacement):r;(10,3+posdisplacement):r;	
}
Drei = {
	(5,0+posdisplacement):r;(5,1+posdisplacement):r;(5,2+posdisplacement):r;	
																			(6,3+posdisplacement):r;	
																			(7,3+posdisplacement):r;	
													(8,2+posdisplacement):r;
																			(9,3+posdisplacement):r;
	(10,0+posdisplacement):r;(10,1+posdisplacement):r;(10,2+posdisplacement):r;	
}
Vier = {
	(5,0+posdisplacement):r;												(5,3+posdisplacement):r;														
	(6,0+posdisplacement):r;												(6,3+posdisplacement):r;	
	(7,0+posdisplacement):r;(7,1+posdisplacement):r;(7,2+posdisplacement):r;(7,3+posdisplacement):r;	
																			(8,3+posdisplacement):r;	
																			(9,3+posdisplacement):r;	
																			(10,3+posdisplacement):r;	
}
Fuenf = {
							(5,1+posdisplacement):r;(5,2+posdisplacement):r;(5,3+posdisplacement):r;	
	(6,0+posdisplacement):r;
							(7,1+posdisplacement):r;(7,2+posdisplacement):r;
																			(8,3+posdisplacement):r;
																			(9,3+posdisplacement):r;	
	(10,0+posdisplacement):r;(10,1+posdisplacement):r;(10,2+posdisplacement):r;	
}
Sechs = {
							(5,1+posdisplacement):r;(5,2+posdisplacement):r;(5,3+posdisplacement):r;	
	(6,0+posdisplacement):r;
	(7,0+posdisplacement):r;(7,1+posdisplacement):r;(7,2+posdisplacement):r;
	(8,0+posdisplacement):r;												(8,3+posdisplacement):r;
	(9,0+posdisplacement):r;												(9,3+posdisplacement):r;	
							(10,1+posdisplacement):r;(10,2+posdisplacement):r;
}
Sieben = {
	(5,0+posdisplacement):r;(5,1+posdisplacement):r;(5,2+posdisplacement):r;(5,3+posdisplacement):r;
																			(6,3+posdisplacement):r;	
													(7,2+posdisplacement):r;
													(8,2+posdisplacement):r;
							(9,1+posdisplacement):r;
							(10,1+posdisplacement):r;
}
Acht = {
							(5,1+posdisplacement):r;(5,2+posdisplacement):r;
	(6,0+posdisplacement):r;												(6,3+posdisplacement):r;
							(7,1+posdisplacement):r;(7,2+posdisplacement):r;
	(8,0+posdisplacement):r;												(8,3+posdisplacement):r;
	(9,0+posdisplacement):r;												(9,3+posdisplacement):r;
							(10,1+posdisplacement):r;(10,2+posdisplacement):r;
}
Neun = {
							(5,1+posdisplacement):r;(5,2+posdisplacement):r;
	(6,0+posdisplacement):r;												(6,3+posdisplacement):r;
	(7,0+posdisplacement):r;												(7,3+posdisplacement):r;
							(8,1+posdisplacement):r;(8,2+posdisplacement):r;(8,3+posdisplacement):r;
																			(9,3+posdisplacement):r;
							(10,1+posdisplacement):r;(10,2+posdisplacement):r;
}
Null = {
							(5,1+posdisplacement):r;(5,2+posdisplacement):r;
	(6,0+posdisplacement):r;												(6,3+posdisplacement):r;
	(7,0+posdisplacement):r;												(7,3+posdisplacement):r;
	(8,0+posdisplacement):r;												(8,3+posdisplacement):r;
	(9,0+posdisplacement):r;												(9,3+posdisplacement):r;
							(10,1+posdisplacement):r;(10,2+posdisplacement):r;
}
display.set_m(Eins)
