#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int data;
    struct node *next;
} node;

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

void display(node *head)
{
    printf("HEAD -> ");    
    node *temp = head;
    while (temp != NULL)
    {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }    
    printf("NULL\n");
}

int search(node *head, int val)
{
    node *temp;
    temp=head;
    int pos=-1;
    int count=1;
    while(temp != NULL)
    {
        if (temp->data==val)
        {
            pos=count;
        }
        count++;
        temp=temp->next;
    }
    return pos;   
}

void push(node **head, int val ,node **top)
{
    node *new = (node *)malloc(sizeof(node));
    new->data = val;
    new->next = NULL;
    new->next = *head;
    *head = new;
    *top = new;
}

void pop(node **head,node **top)
{
    node *temp;
    temp=*head;
    *head=temp->next;
    *top=temp->next;
    free(temp);
}

int main()
{
    node *head = NULL, *top = NULL;
    int i, n_size;
    
    printf("How many elements do you want to insert: ");
    scanf("%d", &n_size);
    
    for (i = 1; i <= n_size; i++)
    {
        node *new = (node *)malloc(sizeof(node));
        printf("Please enter value %d: ", i);
        scanf("%d", &new->data);
        new->next = NULL;
        
        if (head == NULL)
        {
            head = new;
            new->next=NULL;
            top = new;
        }
        else
        {
            new->next = head;
            head = new;
            top = new;
        }
    }
    printf("The Stack has been created.\n");

    int opt;
    do
    {
     options();
     printf("---> ");
     scanf("%d",&opt);

     if(opt==1)
     {
        //dislaying
        display(head);
     }
     else if(opt==2)
     {
        //searching
        printf("Please enter the value you want to search :");
        int search_val,pos;
        scanf("%d",&search_val);
        pos=search(head,search_val);
        if(pos==-1)
        {
            printf("%d is not present in the Stack \n",search_val);
        }
        else
        {
            printf("%d is present at position %d in the stack \n",search_val,pos);
        }     
     }
     else if(opt==3)
     {
        //push
        printf("Please enter the element you want to push :");
        int push_val;
        scanf("%d",&push_val);
        push(&head,push_val,&top);
        printf("The Stack has been updated\n");
     }
     else if(opt==4)
     {
        if(head==NULL)
        {
            printf(" Cannot perform POP\n The stack is empty\n Use PUSH to insert some values\n");
        }
        else
        {
            pop(&head,&top);
            printf("The stack has been updated\n");
        }
     }
     else if(opt==5)
     {
        printf("EXITED\n");
     }
     else
     {
        printf("Invalid option\n");
     }  
    } while (opt!=5);

    return 0;
}