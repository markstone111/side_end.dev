//Stack imlementation using array in c language
#include <stdio.h>

void options()
{
    printf("+----------------------------------------------------+\n");
    printf("| Please select an option                            |\n");
    printf("| 1) Display                                         |\n");
    printf("| 2) Search                                          |\n");
    printf("| 3) Push                                            |\n");
    printf("| 4) Pop                                             |\n");
    printf("| 5) Exit                                            |\n");
    printf("+----------------------------------------------------+\n");
}

void display(int arr[],int arr_size)
{
    int i;
    for (i=0;i<arr_size;i++)
    {
        printf(" %d ",arr[i]);
    }
    printf("\n");
}

void search (int arr[],int arr_size,int val)
{
    int flag=0;
    int i,index;
    for (i=0;i<=arr_size-1;i++)
    {
        if(arr[i]==val)
        {
            flag=1;
            index=i;
            break;
        }
    }
    if(flag==1)
    {
        printf("%d is present at index %d in the array\n",val,index);
    }else
    {
        printf("%d is not present in the array\n",val);
    }
}

void push(int arr[],int *top,int val)
{
    *top=*top+1;
    arr[*top]=val;
}

void pop(int arr[],int *top)
{
    arr[*top]=0;
    *top=*top-1;;
}
//If you find this helpful then please recommend this to your friends. 
int main()
{
    printf("Please enter the size of stack :");
    int s_size;
    scanf("%d",&s_size);
    
    int i,val,top;
    top=-1;
    int arr[s_size];
    
    printf("PLEASE ENTER 0 FOR EMPTY VALUES\n");
    for(i=0;i<s_size;i++)
    {
        printf("Please enter value %d :",i+1);
        scanf("%d",&val);
        arr[i]=val;
    }
    for (i=s_size-1;i>=0;i--)
    {
        if(arr[i]!=0)
        {
            top=i;
            break;
        }
    }
    printf("The stack has been created\n");
int opt;
do
{
    options();
    printf("---> ");
    scanf("%d",&opt);
    if(opt==1)
    {
        //displaying
        display(arr,s_size);
    }
    else if(opt==2)
    {
        //searching
        printf("Please enter the value you want to search :");
        int search_val;
        scanf("%d",&search_val);
        search(arr,s_size,search_val);
    }
    else if(opt==3)
    {
        //push
        if(top==s_size-1)
        {
            printf("Cannot perform PUSH\nThe stack is already full\n Use POP to create space\n");
        }
        else
        {
            printf("Please enter the value you want to PUSH ");
            int push_val;
            scanf("%d",&push_val);
            push(arr,&top,push_val);
            printf("The stack has been updated \n");
        }
    }
    else if(opt==4)
    {
        //pop
        if(top==-1)
        {
            printf(" Cannnot perform POP\n The Stack is empty\n Use PUSH to insert some values\n");
        }
        else
        {
            pop(arr,&top);
        }
    }
    else if(opt==5)
    {
        printf("EXITED\n");
    }
    else
    {
        printf("Invalid Option\n");
    }
} while (opt!=5);

    return 0;
}
