function [x, y] = readTSP(filename)

    fileID = fopen(filename, 'r');

    while true
        line = fgetl(fileID);
        if startsWith(line, 'NODE_COORD_SECTION')
            break;
        end
    end

    x = [];
    y = [];

    while ~feof(fileID)
        line = fgetl(fileID);

        if startsWith(line, 'EOF')
            break;
        end

        data = str2double(strsplit(line));

        x = [x, data(2)];  % x坐标在第二列
        y = [y, data(3)];  % y坐标在第三列
    end

    fclose(fileID);
end