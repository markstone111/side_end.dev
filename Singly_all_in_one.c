#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int data;
    struct node *next;
} node;

node *head = NULL, *tail = NULL;


void create(){
	int i, n_size;

    printf("How many elements do you want to insert: ");
    scanf("%d", &n_size);

    for (i = 1; i <= n_size; i++)
    {
        node *new_node = (node *)malloc(sizeof(node));
        printf("Please enter value %d: ", i);
        scanf("%d", &new_node->data);
        new_node->next = NULL;

        if (head == NULL)
        {
            head = new_node;
            tail = new_node;
        }
        else
        {
            tail->next = new_node;
            tail = new_node;
        }
    }

    printf("The linked list has been created.\n");

}


void display(){
	printf("HEAD -> ");

    node *temp = head;
    while (temp != NULL)
    {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }

    printf("NULL\n");

}


void search(){

    // printf("To search, first you have to create lisk first\n");
	// int i, n_size,val,flag;

    // printf("How many elements do you want to insert: ");
    // scanf("%d", &n_size);

    // for (i = 1; i <= n_size; i++)
    // {
    //     node *new_node = (node *)malloc(sizeof(node));
    //     printf("Please enter value %d: ", i);
    //     scanf("%d", &new_node->data);
    //     new_node->next = NULL;

    //     if (head == NULL)
    //     {
    //         head = new_node;
    //         tail = new_node;
    //     }
    //     else
    //     {
    //         tail->next = new_node;
    //         tail = new_node;
    //     }
    // }

    // printf("The linked list has been created.\n");
    printf("Enter the element you want to search :");
    int val;
    scanf("%d",&val);
    node *temp;
    temp=head;
    int flag=0;
    while(temp != NULL)
    {
        if (temp->data==val)
        {
            flag=1;
        }
        temp=temp->next;
    }
    if(flag==1)
    {
        printf("%d is present in list\n",val);
    }else
    {
        printf("%d is not present in list\n",val);
    }


}

void insert(){
	void options()
{
    printf("Select where you want to perform insert\n");
    printf("1) At Beginning\n");
    printf("2) At Middle\n");
    printf("3) At End\n");
}

// 	int n_size;
// 	printf("how many elements you wnat to insert: ");
//     scanf("%d", &n_size);
// 	int i;
//     // Create initial linked list
//     for (i = 1; i <= n_size; i++)
//     {
//         node *new_node = (node *)malloc(sizeof(node));
//         printf("Please enter value %d: ", i);
//         scanf("%d", &new_node->data);
//         new_node->next = NULL;

//         if (head == NULL)
//         {
//             head = new_node;
//             tail = new_node;
//         }
//         else
//         {
//             tail->next = new_node;
//             tail = new_node;
//         }
//     }
//     int opt,val,pos;
//     printf("The linked list has been created.\n");

    // Print initial list
    int val,i,opt,pos;
    node *temp = head;
    printf("HEAD ->");
    while (temp != NULL)
    {
        printf(" %d ->", temp->data);
	        temp = temp->next;
    }
    printf(" NULL\n");

    // Choose insertion option
    options();
    scanf("%d", &opt);

    printf("Enter the value you want to insert: ");
    scanf("%d", &val);

    node *new_node = (node *)malloc(sizeof(node));
    new_node->data = val;
    new_node->next = NULL;

    if (opt == 1)
    {
        // Insert at the beginning
        new_node->next = head;
        head = new_node;
    }
    else if (opt == 2)
    {
        // Insert at the middle
        printf("Enter the position after which to insert : ");
        scanf("%d", &pos);

        // if (pos < 1 || pos > n_size)
        // {
        //     printf("Invalid position.\n");
        //     free(new_node);
        // }
        // else
        // {
        //     node *temp = head;
        //     for (i = 1; i < pos; i++)
        //     {
        //         temp = temp->next;
        //     }

        //     new_node->next = temp->next;
        //     temp->next = new_node;
        // }
    }
    else if (opt == 3)
    {
        // Insert at the end
        tail->next = new_node;
        tail = new_node;
    }
	 else
    {
        printf("Please select a valid option\n");
        free(new_node);
    }

    // Print updated list
    printf("The linked list has been updated.\n");
    temp = head;
    printf("HEAD ->");
    while (temp != NULL)
    {
        printf(" %d ->", temp->data);
        temp = temp->next;
    }
    printf(" NULL\n");



	
}

void delete(){
	void options()
{
    printf("Select from where you want to perform delete\n");
    printf("1) At Beginning (Will delete first element)\n");
    printf("2) At Middle\n");
    printf("3) At End\n");
}
    int i, n_size, opt, pos;

    // printf("How many elements do you want to insert: ");
    // scanf("%d", &n_size);

    // // Create the linked list
    // for (i = 1; i <= n_size; i++)
    // {
    //     node *new_node = (node *)malloc(sizeof(node));
    //     printf("Please enter value %d: ", i);
    //     scanf("%d", &new_node->data);
    //     new_node->next = NULL;

    //     if (head == NULL)
    //     {
    //         head = new_node;
    //         tail = new_node;
    //     }
    //     else
    //     {
    //         tail->next = new_node;
    //         tail = new_node;
    //     }
    // }

    // // Display the created linked list
    // printf("The linked list has been created.\nHEAD -> ");
    node *temp = head;
    while (temp != NULL)
    {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
	    printf("NULL\n");

    options();
    scanf("%d", &opt);

    if (opt == 1)
    {
        // Deletion at the beginning
        if (head != NULL)
        {
            node *temp = head;
            head = head->next;
            free(temp);
        }
    }
    else if (opt == 2)
    {
        // Deletion in the middle
        printf("Enter the position to delete (1 to %d): ", n_size);
        scanf("%d", &pos);

        if (pos < 1 || pos > n_size)
        {
            printf("Invalid position.\n");
        }
        else if (pos == 1)
        {
            // If position is 1, it's the same as deleting the first element
            node *temp = head;
            head = head->next;
            free(temp);
        }
        else
        {
            node *prev = head;
            for (i = 1; i < pos - 1; i++)
            {
                prev = prev->next;
            }

            node *to_delete = prev->next;
            prev->next = to_delete->next;
            free(to_delete);
        }
    }
    else if (opt == 3)
    {
        // Deletion at the end
        if (head != NULL)
        {

	            if (head->next == NULL)
            {
                // If there's only one element, head becomes NULL
                free(head);
                head = NULL;
            }
            else
            {
                node *temp = head;
                while (temp->next->next != NULL)
                {
                    temp = temp->next;
                }

                node *to_delete = temp->next;
                temp->next = NULL;
                free(to_delete);
            }
        }
    }
    else
    {
        printf("Invalid Option\n");
    }
    if (opt==1||opt==2||opt==3)
    {
        // Display the updated linked list
        printf("The linked list has been updated.\nHEAD -> ");
        temp = head;
        while (temp != NULL)
        {
            printf("%d -> ", temp->data);
            temp = temp->next;
        }
        printf("NULL\n");
    }

}


int main()
{
	create();
	printf("Choose the option :\n1) for display.\n2) for deletion.\n3) for insertion.\n4) for searching.\n5) for exit.\n");
	int option;
	scanf("%d",&option);
	if(option==1){
		display();}
	else if(option==3){
		insert();}
	else if(option==2){
		delete();}
	else if(option==4){
		search();}
	else if(option==5){
    	}
	else{
		printf("invald option");}
    	
	return 0;
}
