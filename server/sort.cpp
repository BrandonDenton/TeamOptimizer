#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

class Sort{
	public:
		// initializes the class population's Myer's Briggs Types
		Sort(int csize, int gsize, double pe, double ps, double pt, double pj);
		// prints out the class population's Myer's Briggs Types
		void print();
		void run();
	protected:
		vector <vector <char> > studentMB; // Myer's Briggs scores of the class
		int classSize;
		int groupSize;
		double percentE;				   // Probability of being E
		double percentS;				   // Probability of being S
		double percentT;				   // Probability of being T
		double percentJ;				   // Probability of being J
};

Sort::Sort(int csize, int gsize, double pe, double ps, double pt, double pj){
	int i, j;
	int E, S, T, J;
	char types[8] = {'E', 'I', 'S', 'N', 'T', 'F', 'J', 'P'};

	classSize = csize;
	groupSize = gsize;
	percentE = pe;
	percentS = ps;
	percentT = pt;
	percentJ = pj;

	studentMB.resize(classSize);
	for (i = 0; i < classSize; i++){
		studentMB[i].resize(4);
	}
	
	// initialize students' MB scores randomly based on probabilities given
	srand(0);
	//srand(time(NULL));
	E = S = T = J = 0;
	for (i = 0; i < classSize; i++){
		for (j = 0; j < 4; j++){
			switch (j){
				case 0:
					if (rand()%100 < percentE){
						studentMB[i][j] = types[j*2];
						E++;
					}else{
						studentMB[i][j] = types[1+j*2];
					}
					break;
				case 1:
					if (rand()%100 < percentS){
						studentMB[i][j] = types[j*2];
						S++;
					}else{
						studentMB[i][j] = types[1+j*2];
					}
					break;
				case 2:
					if (rand()%100 < percentT){
						studentMB[i][j] = types[j*2];
						T++;
					}else{
						studentMB[i][j] = types[1+j*2];
					}
					break;
				case 3:
					if (rand()%100 < percentJ){
						studentMB[i][j] = types[j*2];
						J++;
					}else{
						studentMB[i][j] = types[1+j*2];
					}
					break;
			}
		}
	}

	printf("Actual E/I, S/N, T/F, J/P in class generated from possibilities\n");
	printf("E = %d (%lg%c), I = %d (%lg%c)\n", E, (double)E/classSize*100, '%', classSize - E, (double)(classSize - E)/classSize*100, '%');
	printf("S = %d (%lg%c), N = %d (%lg%c)\n", S, (double)S/classSize*100, '%', classSize - S, (double)(classSize - S)/classSize*100, '%');
	printf("T = %d (%lg%c), F = %d (%lg%c)\n", T, (double)T/classSize*100, '%', classSize - T, (double)(classSize - T)/classSize*100, '%');
	printf("J = %d (%lg%c), P = %d (%lg%c)\n", J, (double)J/classSize*100, '%', classSize - J, (double)(classSize - J)/classSize*100, '%');
	printf("\n");

}

void Sort::print(){
	int i, j;

	printf("Students' Myer's Briggs Scores:\n");
	for (i = 0; i < classSize; i++){
		for (j = 0; j < 4; j++){
			printf("%c", studentMB[i][j]);
		}
		printf("\n");
	}
}

void Sort::run(){
	print();
}

int main(int argc, char **argv){
	int csize, gsize;
	istringstream ss;
	double pe, ps, pt, pj;

	if (argc < 6){
		fprintf(stderr, "usage: number of students in class, number of students per group, percent of extroverts, percent of sensing, percent of thinking, percent of judging\n");
		return -1;
	}
	ss.clear();
	ss.str(argv[1]);
	if ( (!(ss >> csize)) || (csize <= 1)){
		fprintf(stderr, "usage: number of students in class must be an integer greater than 1\n");
		return -1;
	}
	ss.clear();
	ss.str(argv[2]);
	if ( (!(ss >> gsize)) || (gsize <= 0) ){
		fprintf(stderr, "usage: group size must be an integer greater than 0\n");
		return -1;
	}
	ss.clear();
	ss.str(argv[3]);
	if ( (!(ss >> pe)) || (pe < 0) || (pe > 100) ){
		fprintf(stderr, "usage: percent extroverts must be a number between 0-100\n");
		return -1;
	}
	ss.clear();
	ss.str(argv[4]);
	if ( (!(ss >> ps)) || (ps < 0) || (ps > 100) ){
		fprintf(stderr, "usage: percent sensing must be a number between 0-100\n");
		return -1;
	}
	ss.clear();
	ss.str(argv[5]);
	if ( (!(ss >> pt)) || (pt < 0) || (pt > 100) ){
		fprintf(stderr, "usage: percent thinking must be a number between 0-100\n");
		return -1;
	}
	ss.clear();
	ss.str(argv[6]);
	if ( (!(ss >> pj)) || (pj < 0) || (pj > 100) ){
		fprintf(stderr, "usage: percent judging must be a number between 0-100\n");
		return -1;
	}
	
	// print to stdout command line arg read
	printf("Number of students in class: %d\n", csize);
	printf("Number of students per group: %d\n", gsize);
	printf("Possibilities of being E and I: %lg%c E, %lg%c I\n", pe, '%', 100.0-pe, '%');
	printf("Possibilities of being S and N: %lg%c S, %lg%c N\n", ps, '%', 100.0-ps, '%');
	printf("Possibilities of being T and F: %lg%c T, %lg%c F\n", pt, '%', 100.0-pt, '%');
	printf("Possibilities of being J and P: %lg%c J, %lg%c P\n", pj, '%', 100.0-pj, '%');
	printf("\n");

	Sort sort(csize, gsize, pe, ps, pt, pj);
	sort.run();

	return 0;
}

