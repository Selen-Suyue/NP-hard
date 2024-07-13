function L = tourLength(tour,model)
tour = [tour, tour(1)];
N = model.N;
L = 0;
for i = 1:N
    L = L + model.D(tour(i),tour(i+1));
end 
end

