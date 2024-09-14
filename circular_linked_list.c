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
            tail->next=head;
        }
        else
        {
            tail->next = new_node;
            tail = new_node;
            tail->next=head;
            
        }
    }

    printf("The Circular linked list has been created.\n");

}


void display(){
	printf("HEAD -> ");

    node *temp = head;
    do
    {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }while(temp!=head);

    printf("NULL\n");

}


void search(){
    printf("Enter the element you want to search :");
    int val;
    scanf("%d",&val);
    node *temp;
    temp=head;
    int flag=0;
    do
    {
        if (temp->data==val)
        {
            flag=1;
        }
        temp=temp->next;
    }while(temp != head);
    if(flag==1)
    {
        printf("%d is present in circular linked list\n",val);
    }else
    {
        printf("%d is not present in circular linked list\n",val);
    }


}



void insert() {
    void options() {
        printf("Select where you want to perform insert\n");
        printf("1) At Beginning\n");
        printf("2) At Middle\n");
        printf("3) At End\n");
    }

    int val, i, opt, pos;
    node *temp = head;

    // Print initial list
    printf("HEAD ->");
    if (head != NULL) {
        do {
            printf(" %d ->", temp->data);
            temp = temp->next;
        } while (temp != head);
    }
    printf(" HEAD\n");

    // Choose insertion option
    options();
    scanf("%d", &opt);

    printf("nter the value you want to insert: ");
    scanf("%d", &val);
    node *new_node = (node *)malloc(sizeof(node));
    new_node->data = val;

    if (opt == 1) {
        // Insert at the beginning
        new_node->next = head;
        head = new_node;
        tail->next = head; // Circular adjustment
    } else if (opt == 2) {
        // Insert at the middle
        printf("Enter the posiriom after which to insert: ");
        scanf("%d", &pos);
        node *temp = head;
        for (i = 1; i < pos; i++) {
            temp = temp->next;
        }
        new_node->next = temp->next;
        temp->next = new_node;
    } else if (opt == 3) {
        // Insert at the end
        tail->next = new_node;
        tail = new_node;
        tail->next = head;
    } else {
        printf("Please select a valid option\n");
        free(new_node);
        return;
    }

    // Print updated list
    printf("The linked list has been updated.\n");
    temp = head;
    printf("HEAD ->");
    do {
        printf(" %d ->", temp->data);
        temp = temp->next;
    } while (temp != head);
    printf(" HEAD\n");
}

void delete() {
    void options() {
        printf("Select from where you want to perform delete\n");
        printf("1) At Beginning (Will delete first element)\n");
        printf("2) At Middle\n");
        printf("3) At End\n");
    }

    int i, opt, pos;

    node *temp = head;
    if (head == NULL) {
        printf("List is empty.\n");
        return;
    }

    printf("Head -> ");
    do {
        printf("%d -> ", temp->data);
        temp = temp->next;
    } while (temp != head);
    printf("\n");

    options();
    scanf("%d", &opt);

    if (opt == 1) {
        // Deletion at the beginning
        if (head != NULL) {
            node *temp = head;
            if (head == tail) {
                // If there's only one node in the list
                head = tail = NULL;
            } else {
                head = head->next;
                tail->next = head; // Circular adjustment
            }
            free(temp);
        }
    }
    else if (opt == 2) {
        // Deletion in the middle
        printf("Enter the position to delete: ");
        scanf("%d", &pos);

        if (pos == 1) {
            // If position is 1, it's the same as deleting the first element
            node *temp = head;
            if (head == tail) {
                head = tail = NULL;
            } else {
                head = head->next;
                tail->next = head;
            }
            free(temp);
        } else {
            node *prev = head;
            for (i = 1; i < pos - 1; i++) {
                prev = prev->next;
            }
            node *q = prev->next;
            prev->next = q->next;
            free(q);
        }
    }
    else if (opt == 3) {
        // Deletion at the end
        if (head != NULL) {
            if (head == tail) {
                // Only one node in the list
                free(head);
                head = tail = NULL;
            } else {
                node *temp = head;
                while (temp->next != tail) {
                    temp = temp->next;
                }
                node *to_delete = tail;
                temp->next = head; // Maintain circular structure
                tail = temp;
                free(to_delete);
            }
        }
    } 
    else {
        printf("Invalid Option\n");
        return;
    }

    // Display the updated linked list
    if (head == NULL) {
        printf("The linked list is now empty.\n");
    } else {
        printf("The linked list has been updated.\nHEAD -> ");
        temp = head;
        do {
            printf("%d -> ", temp->data);
            temp = temp->next;
        } while (temp != head);
        printf("HEAD\n");
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