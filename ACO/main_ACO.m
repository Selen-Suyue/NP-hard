clc; clear; close all;

% 指定文件夹路径
folderPath = './data/';

% 获取文件夹中的文件列表
files = dir(fullfile(folderPath, '*.tsp'));
files.name

% 遍历所有文件
for i = 1:length(files)
    close all;
    [tsp_name, ~] = strtok(files(i).name, '.');

    % 读取坐标
    [x, y] = readTSP([folderPath, tsp_name, '.tsp']);
    iter_lengths = [];
    best_iter.length = inf;
    best_iter.tour = [];

    for idx = 1:10
        %% 1-优化问题的定义
        model = creatModel(x, y);
        costFunction = @(tour) tourLength(tour,model);
        N = model.N;
        %% 2-DE参数的定义
        max_iter = 500;
        npop = 100;
        alpha = 1;
        beta = 4;
        Q = 1;
        rho = 0.1;
        
        %% 3-DE的初始化
        tau = ones(N,N);
        eta = 1./model.D;
        empty_ant.tour = [];
        empty_ant.length = [];
        ant = repmat(empty_ant,npop);
        best_ant.length = inf; 
        
        %% 4-DE的主循环部分
        for iter = 1:max_iter
        
            for i = 1:npop
                ant(i).tour = randi([1,N]); % 起点随机
        
                for j = 2:N
                    tourlast = ant(i).tour(end); % 上一个点为下一个点选择的起点
                    P = tau(tourlast,:).^alpha.*eta(tourlast,:).^beta; % 计算上一个点到每个点的概率
                    % P(P < threshold) = threshold;
                    P(ant(i).tour) = 0; % 已访问地址置零
                    P = P/sum(P); 
                    m = rouletWheelSelection(P); % 轮盘选择下一个点
                    ant(i).tour =[ant(i).tour, m]; % 将下一个点添加的路径中
                end
                ant(i).length = costFunction(ant(i).tour); % 计算长度
                if ant(i).length<best_ant.length
                    best_ant = ant(i);
                end
            end
        
            for i = 1:npop
                tour = ant(i).tour;
                tour = [tour, tour(1)];
        
                for j = 1:N
                    m = tour(j);
                    n = tour(j+1);
                    tau(m,n) = tau(m,n) + Q/ant(i).length; % 信息素更新
                end
                
            end
            tau = (1 - rho)*tau; % 信息素衰减
            Convergence_Curve(iter) = best_ant.length;
            disp(['迭代次数 = ', num2str(iter), '最佳适应度值 = ', num2str(best_ant.length)])
        end
        
        %% 5-优化结果的处理
        plotPath(x, y, best_ant.tour, best_ant.length, tsp_name, num2str(idx)); % 画路径

        iter_lengths = [iter_lengths, best_ant.length];
        if best_ant.length < best_iter.length % 找出最佳解
            best_iter.tour = best_ant.tour;
            best_iter.length = best_ant.length
        end
    end
    
    plotPath(x, y, best_iter.tour, best_iter.length, tsp_name, 'best');

     % 找到最小值及其索引
    [minValue, minIndex] = min(iter_lengths);
    
    % 找到最大值及其索引
    [maxValue, maxIndex] = max(iter_lengths);
    
    % 计算均值和标准差
    meanValue = mean(iter_lengths);
    stdDeviation = std(iter_lengths);
    
     % 绘制折线图
    plot(1:10, iter_lengths, '-o');
    hold on;
    
    % 标记最小值
    scatter(minIndex, minValue, 'r', 'filled', 'DisplayName', ['最佳解: ' num2str(minValue)]);

    % 标记最大值
    scatter(maxIndex, maxValue, 'g', 'filled', 'DisplayName', ['最差解: ' num2str(maxValue)]);

    % 标记均值
    plot([1, 10], [meanValue, meanValue], 'b--', 'DisplayName', ['均值: ' num2str(meanValue)]);

    % 标记标准差
    plot([1, 10], [meanValue + stdDeviation, meanValue + stdDeviation], 'm--', 'DisplayName', ['均值+标准差: ' num2str(meanValue + stdDeviation)]);
    plot([1, 10], [meanValue - stdDeviation, meanValue - stdDeviation], 'm--', 'DisplayName', ['均值-标准差: ' num2str(meanValue - stdDeviation)]);

    xlabel('迭代次数');
    ylabel('最佳适应度值');
    
    title(sprintf('%s 数组值及统计信息\n最佳解: %s, 最差解: %s, 均值: %s, 标准差: %s\n', tsp_name, num2str(minValue), num2str(maxValue), num2str(meanValue), num2str(stdDeviation)));
        
    legend('最佳适应度值', '最优解');
        
    grid on;
    
     
    % 保存图像到指定路径和文件名
    fileName = sprintf('./img/%s_result.png', tsp_name);
    
    % 使用 saveas 函数保存图像
    saveas(gcf, fileName);
        
    hold off;
    
end



