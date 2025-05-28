
function result = simple_plot()
    x = 0:0.1:2*pi;
    y = sin(x);
    figure;
    plot(x, y);
    title('Sine Wave');
    xlabel('x');
    ylabel('sin(x)');
    result = struct('status', 'success');
end