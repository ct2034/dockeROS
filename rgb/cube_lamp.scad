edge = 80;
width = 1;

union(){
    linear_extrude(height = width)
        square([edge, edge], [0,0]);
    linear_extrude(height = edge)
        square([edge, width]);
    linear_extrude(height = edge)
        square([width, edge]);
    translate([0, edge-width, 0])
        linear_extrude(height = edge)
            square([edge, width]);
    translate([edge-width, 0, 0])
        linear_extrude(height = edge)
            square([width, edge]);
}