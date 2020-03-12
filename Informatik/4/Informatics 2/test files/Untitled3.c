#include <SDL2/SDL.h>
SDL_Window *win;
SDL_Renderer *ren;
float x, y, u;
void l(float dx, float dy) {
	SDL_RenderDrawLine(ren, x, y, x+dx, y+dy);
	x=x+dx; y=y+dy;
	SDL_Delay(5);
	SDL_RenderPresent(ren);
}

void A(int); void B(int); void C(int); void D(int);
void A(int i) {
	if (i>0) {
		B(i-1); l(-u,0);
		A(i-1); l(0,u);
		A(i-1); l(u,0);
		C(i-1);
	}
}

int main (int argc, char** argv) {
	int d;
	sscanf(argv[1], "%d", &d);
	SDL_CreateWindowAndRenderer(400, 400, 0, &win, &ren);
	SDL_SetRenderDrawColor(ren, 255, 255, 255, 0);
	x=395; y=5; u=390/(pow(2,d)-1);
	A(d);
	SDL_Event e;
	do { SDL_PollEvent(&e); } while (e.type != SDL_QUIT);
}

