#include<cstdio>
#include<algorithm>
using namespace std;

//定义方向
const int dirc[5][2] = {{0,0}, {-1,0}, {0, 1}, {1, 0}, {0, -1}};
int H, W, N;
int food[1000][2];
int snake[100000][2];
int map[100][100];
int main(){
    scanf("%d%d%d", &H, &W, &N);
    map[0][0] = 1;
    for (int i = 0; i < N; i++){
        scanf("%d%d", &food[i][0], &food[i][1]);
    }
    int l = 0, r = 0, i = 0;
    while(i < N && map[food[i][0]][food[i][1]]==1) i++;

    //循环直到食物吃完
    while(i < N){
        //选择一个目标方向
        int target = 0;
        if (food[i][0] < snake[r][0]){
            target = 1;
        }else if (food[i][0] > snake[r][0]){
            target = 3;
        }else if (food[i][1] < snake[r][1]){
            target = 4;
        }else if (food[i][1] > snake[r][1]){
            target = 2;
        }


        if (target){
            int next[2];//下一步的位置
            next[0] = snake[r][0] + dirc[target][0];
            next[1] = snake[r][1] + dirc[target][1];
            //如果会撞到自己就原地不动，否则前进一步
            if (map[next[0]][next[1]] == 1){
                target = 0;
            }else{
                map[next[0]][next[1]] = 1;
                r++;
                snake[r][0] = next[0];
                snake[r][1] = next[1];
            }
        }
        printf("%d\n", target);

        //判断食物是否跟蛇重合
        bool eat = false;
        while(i < N && map[food[i][0]][food[i][1]]==1){
            i++;
            eat = true;
        }
        //如果没有吃到食物且长度超过1就缩短
        if (l!=r and eat == false){
            map[snake[l][0]][snake[l][1]] = 0;
            l++;
        }
    }
    printf("Over\n");
}