function plotPath(x, y, pathOrder, pathLength, file_path, name)
    % 绘制坐标点和路径
    
    % 创建新图形
    figure;

    % 绘制散点图表示坐标点，并标出序号
    scatter(x, y, 'filled');
    hold on;  % 保持图形，以便后续绘制路径

    for i = 1:length(x)
        text(x(i), y(i), num2str(i), 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
    end

    % 绘制路径
    for i = 1:length(pathOrder)-1
        startIdx = pathOrder(i);
        endIdx = pathOrder(i+1);
        plot([x(startIdx), x(endIdx)], [y(startIdx), y(endIdx)], 'k-', 'LineWidth', 2);
    end

    % 连接路径的最后一个点和第一个点，形成闭合路径
    startIdx = pathOrder(end);
    endIdx = pathOrder(1);
    plot([x(startIdx), x(endIdx)], [y(startIdx), y(endIdx)], 'k-', 'LineWidth', 2);

    % 添加坐标轴标签
    xlabel('X坐标');
    ylabel('Y坐标');

    % 创建图标题，包含文件路径和路径长度信息
    titleText = sprintf('%s 按照路径顺序绘制的坐标点 (PathLength: %d)', file_path, pathLength);
    title(titleText);

    % 添加图例，标识散点和路径
    legend('点', '路径', 'Location', 'Best');

    % 保存图像到指定路径和文件名
    fileName = sprintf('./img/%s_%s.png', file_path, name);

    % 使用 saveas 函数保存图像
    saveas(gcf, fileName);

    % 取消保持图形状态
    hold off;
end
