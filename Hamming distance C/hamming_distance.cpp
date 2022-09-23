#include <string>
#include <fstream>
#include <vector>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <numeric>


void fill_vector_lines(std::string &file_name, std::vector<std::string> &v_lines) { //It has & before v_lines
    std::ifstream input_stream(file_name.c_str());
    std::string line;

    // Read the entire file
    while (std::getline(input_stream, line))
    {
        // Check line is not empty to save in vector
        if(!line.empty())
            v_lines.push_back(line);
    }
    // Close file
    input_stream.close();
}


void split_line(const char delim, std::string &line, std::vector<std::string> &v_str)
{
    std::stringstream string_stream(line);
    std::string sub_str;

    // Split string based on space delimiter and save each element string in vector
    while (std::getline(string_stream, sub_str, delim)) {
        v_str.push_back(sub_str);
    }
}

int hamming_distance(std::string &src_str, std::string &tar_str)
{

    //const char *str_src = str1.c_str();
    //const char *str_trg = str1.c_str();

    int i = 0;
    int count = 0;

    while(src_str[i]!='\0')
    {
        if (src_str[i] != tar_str[i])
            count++;
        i++;
    }
    return count;
}

void compute_distance(int pos, std::vector<std::string> v_str, std::vector<int> &v_dist)
{
    // Calculate distance
    int distance = 0;
    int real_pos = pos -1;

    //std::cout<<"v_str.siye: " <<v_str.size()<<std::endl;

        for(auto i=0; i <= v_str.size() -1 ; i++)
        {
            if (i != real_pos){
                distance = hamming_distance(v_str[real_pos], v_str[i]);
                v_dist.push_back(distance);
                std::cout<<"SRC: " <<v_str[real_pos]<< " TAR: " << v_str[i] << " Distance: " << distance << std::endl;
            }

        }
}

double compute_median(std::vector<int> v_dist){
    sort(v_dist.begin(), v_dist.end());
    double result;
    if(v_dist.size() % 2 == 0)
        result = (v_dist[v_dist.size()/2 - 1] + v_dist[v_dist.size()/2] ) /2;
    else
        result = v_dist[v_dist.size() / 2];
    return result;
}

int compute_occurrency(std::string sub_str, std::vector<std::string> v_str){

    int count = 0;
    for(int i=0; i <= v_str.size() -1 ; i++){
        size_t nPos = v_str[i].find(sub_str, 0); // first occurrence
        while(nPos != std::string::npos)
        {
            count++;
            nPos = v_str[i].find(sub_str, nPos + 1);
        }
    }
    return count;
}


int main(int argc, char** argv) {

    // Variables
    int pos = atoi(argv[1]);
    std::string sub_string = argv[2];
    std::string input_file = argv[3];
    std::string output_file = argv[4];

    const char delimiter = ' ';
    int real_pos = pos -1;


    //std::cout << "Position: " << pos << " Substring: " << sub_string<< " File: " << input_file << std::endl;

    // Vectors
    std::vector<std::string> v_lines;
    std::vector<std::string> v_str;
    std::vector<int> v_dist;

    // Fill vector with lines from input file
    fill_vector_lines(input_file, v_lines);

    // Iterate over vector of lines and ...
    for (int line =0; line <= v_lines.size() - 1; ++line) {
        v_str.clear();
        v_dist.clear();
        std::ofstream out_file(output_file, std::ios_base::app);
        //std::cout<<"Line: " <<v_lines[line]<<std::endl;

        split_line(delimiter, v_lines[line], v_str);

        if (real_pos <= v_str.size() -1 ){
            compute_distance(pos, v_str, v_dist);

            out_file << *std::min_element(std::begin(v_dist), std::end(v_dist)) << " "
                     << *std::max_element(std::begin(v_dist), std::end(v_dist)) << " "
                     << std::reduce(v_dist.begin(), v_dist.end()) / static_cast<double>(v_dist.size()) << " "
                     << compute_median(v_dist) << " "
                     << compute_occurrency(sub_string, v_str) << "\n";
            }
        else{
            out_file << "\n";
            }
        out_file.close();
        }
    return 0;
}
