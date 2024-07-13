%轮盘赌选择
function idx = rouletWheelSelection(P)
c = cumsum(P); %累积概率
r = rand; %随机数生成
lth = length(P); %染色体长度

if r<c(1)
    idx = 1;
else
    for i = 2:lth 
        if r>c(i-1) && r<c(i) 
            idx = i;
        end
    end
end

end