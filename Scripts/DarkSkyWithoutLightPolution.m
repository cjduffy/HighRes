number_images = length(dir('*.CR2'));
starting_number = 4076; %change this

A = cell(1,length(dir('*CR2')));
C = zeros(1,number_images)

for j = (starting_number : starting_number + number_images - 1);
    
    A{1,j} = imread(sprintf('IMG_%d.CR2',j));
    
C(1,j-4075) = mean(A{1,j}(:)) %also change the subtracted value as needed
    
end