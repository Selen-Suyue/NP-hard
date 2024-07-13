function model = creatModel(x, y)
    
model.x = x;
model.y = y;
N = length(x);
model.N = N;

D = zeros(N,N);

for i = 1:N
    for j = 1:N 
        D(i,j) = sqrt((x(i)-x(j))^2 + (y(i)-y(j))^2);
    end     
end
model.D = D;
end

