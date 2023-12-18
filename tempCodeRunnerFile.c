#include <iostream>
using namespace std;

class Flight
{
private:
    int Flight_ID;
    string Model;
    int Capacity;
    string Airline;
    string Destination;
    string Departure_time;
    double Ticket_Price;

public:
    Flight() : Flight_ID(0), Model(""), Capacity(0), Airline(""), Destination(""), Departure_time(""), Ticket_Price(0.0) {}
    Flight(int id, string mdl, int cap, string airl, string dest, string deptime, double tckt)
        : Flight_ID(id), Model(mdl), Capacity(cap), Airline(airl), Destination(dest), Departure_time(deptime), Ticket_Price(tckt) {}

    int get_flight_id() const
    {
        return Flight_ID;
    }

    string get_model() const
    {
        return Model;
    }

    int get_capacity() const
    {
        return Capacity;
    }

    string get_airline() const
    {
        return Airline;
    }

    string get_destination() const
    {
        return Destination;
    }

    string get_departure_time() const
    {
        return Departure_time;
    }

    double get_ticket_price() const
    {
        return Ticket_Price;
    }

    void set_flight_id(int id)
    {
        Flight_ID = id;
    }

    void set_model(string mdl)
    {
        Model = mdl;
    }

    void set_capacity(int cap)
    {
        Capacity = cap;
    }

    void set_airline(string airl)
    {
        Airline = airl;
    }

    void set_destination(string dest)
    {
        Destination = dest;
    }

    void set_departure_time(string deptime)
    {
        Departure_time = deptime;
    }

    void set_ticket_price(double tckt)
    {
        Ticket_Price = tckt;
    }

    void display_Flight_info() const
    {
        cout << "Flight ID: " << Flight_ID << endl;
        cout << "Model: " << Model << endl;
        cout << "Capacity: " << Capacity << endl;
        cout << "Airline: " << Airline << endl;
        cout << "Destination: " << Destination << endl;
        cout << "Departure Time: " << Departure_time << endl;
        cout << "Ticket Price: " << Ticket_Price << endl;
    }
};

template <class T>
class Node
{
public:
    T data;
    Node<T> *next;

    Node(T value) : data(value), next(nullptr) {}
};

template <class T>
class FlightList
{
public:
    Node<T> *head;
    FlightList() : head(nullptr) {}

    void AddFlight(T value)
    {
        Node<T> *newNode = new Node<T>(value);

        Node<T> *temp = head;
        while (temp != nullptr)
        {
            if (temp->data.get_flight_id() == value.get_flight_id())
            {
                cout << "Duplicate Flight." << endl;
                return;
            }
            temp = temp->next;
        }

        if (isEmpty())
        {
            head = newNode;
            head->next = nullptr;
        }
        else
        {
            temp = head;
            while (temp->next != nullptr)
            {
                temp = temp->next;
            }
            temp->next = newNode;
            newNode->next = nullptr;
        }
    }

    void DelFlight(int flightid)
    {
        Node<T> *current = head;
        Node<T> *prev = nullptr;

        if (isEmpty())
        {
            cout << "The list is empty" << endl;
        }

        if (!flightExists(flightid))
        {
            cout << "Nothing in the list" << endl;
            return;
        }

        if (flightid == head->data.get_flight_id())
        {
            head = head->next;
            delete current;
        }
        else
        {
            while (current->data.get_flight_id() != flightid && current != nullptr)
            {
                prev = current;
                current = current->next;
            }
            prev->next = current->next;
            delete current;
        }
    }

    void DisplayAll()
    {
        Node<T> *temp = head;

        if (head == nullptr)
            cout << "There is no flights" << endl;

        while (temp != nullptr)
        {
            temp->data.display_Flight_info();
            cout << endl;
            temp = temp->next;
        }
    }

    void InsertNewFlight()
    {
        int id, cap;
        string mdl, airl, dest, deptime;
        double tckt;

        cout << "Enter Flight ID: ";
        cin >> id;
        while (cin.fail())
        {
            cout << "Wrong input" << endl;
            cin.clear();  // Clear the error flag
            cin.ignore(); // Discard invalid input
            cin >> id;
        }
        cout << "Enter Model: ";
        cin.ignore();
        getline(cin, mdl);
        cout << "Enter Capacity: ";
        cin >> cap;
        while (cin.fail())
        {
            cout << "Error: Wrong input" << endl;
            cin.clear();  
            cin.ignore(); 
            cin >> cap;
        }
        cout << "Enter the Airline: ";
        cin.ignore();
        getline(cin, airl);
        cout << "Enter the Destination: ";
        getline(cin, dest);
        cout << "Enter the Departure Time: ";
        getline(cin, deptime);
        cout << "Enter Ticket Price: ";
        cin >> tckt;
        while (cin.fail())
        {
            cout << "Wrong input" << endl;
            cin.clear();  
            cin.ignore(); 
            cin >> tckt;
        }

        Flight newFlight(id, mdl, cap, airl, dest, deptime, tckt);

        AddFlight(newFlight);

        cout << "New Flight added successfully!" << endl;
    }

    bool isEmpty() const
    {
        return (head == nullptr);
    }

    bool flightExists(int key) const
    {
        Node<T> *temp = head;
        bool found = false;

        while (temp != nullptr)
        {
            if (temp->data.get_flight_id() == key)
            {
                found = true;
                break;
            }
            temp = temp->next;
        }
        return found;
    }

    int Count() const
    {
        int counter = 0;
        Node<T> *temp = head;

        while (temp != nullptr)
        {
            counter++;
            temp = temp->next;
        }
        return counter;
    }
};
template <class T>
class FlightStack
{
private:
public:
    Node<T> *TOP;
    FlightStack()
    {
        TOP = NULL;
    }

    void PushFlight(T flight) // Add flight
    {
        Node<T> *newnode = new Node<T>(flight);
        newnode->data = flight;

        Node<T> *temp = TOP;
        while (temp != NULL)
        {
            if (temp->data.get_flight_id() == flight.get_flight_id())// Check if duplicate
            {
                cout << "Duplicate Flight." << endl;
                return;
            }
            temp = temp->next;
        }

        if (isEmpty())
        {
            newnode->next = NULL;
            TOP = newnode;
        }
        else
        {
            newnode->next = TOP;
            TOP = newnode;
        }
    }

    void PrintStack()
    {
        Node<T> *temp = TOP;
        while (temp != NULL)
        {
            temp->data.display_Flight_info();
            cout << endl;
            temp = temp->next;
        }
        cout << endl;
    }

    void Peek() // to see TOP element
    {
        if (!isEmpty())
        {
            TOP->data.display_Flight_info();
        }
        else
        {
            cout << "Stack is empty. Cannot peek.";
        }
    }

    bool isEmpty()
    {
        return (TOP == NULL);
    }

    bool isFound(int id)
    {
        Node<T> *temp = TOP;
        bool found = false;

        while (temp != NULL)
        {
            if (temp->data.get_flight_id() == id)
            {
                found = true;
                break;
            }
            temp = temp->next;
        }
        return found;
    }

    void DeleteStack(int flightid) // delete by flight ID
    {
        Node<T> *current = TOP;
        Node<T> *prev = NULL;

        if (isEmpty())
        {
            cout << "Stack is so far empty" << endl;
        }

        if (!isFound(flightid))
        {
            cout << "there is no something in the stack" << endl;
            return;
        }

        if (flightid == TOP->data.get_flight_id())
        {
            TOP = TOP->next;
            delete current;
        }
        else
        {
            while (current->data.get_flight_id() != flightid && current != NULL)
            {
                prev = current;
                current = current->next;
            }
            prev->next = current->next;
            delete current;
        }
    }

    void EditStack(int flightID) // user choose what exactly to edit in the flight info
    {
        Node<T> *temp = TOP;

        while (temp != NULL)
        {
            if (temp->data.get_flight_id() == flightID)
            {
                cout << "Flight exsist. Enter the name of the attribute to edit:" << endl;
                cout << "1. Flight ID" << endl;
                cout << "2. Model" << endl;
                cout << "3. Capacity" << endl;
                cout << "4. Airline" << endl;
                cout << "5. Destination" << endl;
                cout << "6. Departure Time" << endl;
                cout << "7. Ticket Price" << endl;

                int choice;
                cout << "Enter your choice: ";
                cin >> choice;

                switch (choice)
                {
                case 1:
                {
                    int newID;
                    cout << "Enter the new Flight ID: ";
                    cin >> newID;
                    while (cin.fail()) // to handle if the user inputs string
                    {
                        cout << "Wrong input" << endl;
                        cin.clear();  // Clear the error flag
                        cin.ignore(); // Discard invalid input
                        cin >> newID;
                    }
                    temp->data.set_flight_id(newID);
                    break;
                }

                case 2:
                {
                    string newModel;
                    cout << "Enter the new Model: ";
                    cin.ignore();
                    getline(cin, newModel);
                    temp->data.set_model(newModel);
                    break;
                }

                case 3:
                {
                    int newCapacity;
                    cout << "Enter the new Capacity: ";
                    cin >> newCapacity;
                    while (cin.fail()) // to handle if the user inputs string
                    {
                        cout << "Wrong input" << endl;
                        cin.clear();  
                        cin.ignore(); 
                        cin >> newCapacity;
                    }
                    temp->data.set_capacity(newCapacity);
                    break;
                }

                case 4:
                {
                    string newAirline;
                    cout << "Enter the new Airline: ";
                    cin.ignore();
                    getline(cin, newAirline);
                    temp->data.set_airline(newAirline);
                    break;
                }

                case 5:
                {
                    string newDestination;
                    cout << "Enter the new Destination: ";
                    cin.ignore();
                    getline(cin, newDestination);
                    temp->data.set_destination(newDestination);
                    break;
                }

                case 6:
                {
                    string newDepartureTime;
                    cout << "Enter the new Departure Time: ";
                    cin.ignore();
                    getline(cin, newDepartureTime);
                    temp->data.set_departure_time(newDepartureTime);
                    break;
                }

                case 7:
                {
                    double newTicketPrice;
                    cout << "Enter the new Ticket Price: ";
                    cin >> newTicketPrice;
                    while (cin.fail()) // to handle if the user inputs string
                    {
                        cout << "Wrong input" << endl;
                        cin.clear();  
                        cin.ignore(); 
                        cin >> newTicketPrice;
                    }
                    temp->data.set_ticket_price(newTicketPrice);
                    break;
                }

                default:
                    cout << "wrong choice. No changes did." << endl;
                    return;
                }

                cout << "Flight information edited successfully!" << endl;
                return;
            }

            temp = temp->next;
        }

        cout << "Flight is not in the stack." << endl;
    }
    
    int Count()
    {
        int counter = 0;
        Node<T> *temp = TOP;

        while (temp != NULL)
        {
            counter++;
            temp = temp->next;
        }
        return counter;
    }
};
int main()
{
    cout << "Welcome to the Flight Management System" << endl;

    int choice;

    do
    {
        cout << "\nChoose an option:\n";
        cout << "1. LinkedList\n";
        cout << "2. Stack\n";
        cout << "0. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice)
        {
        case 1:
        {
            FlightList<Flight> flightList;

            int choice;

            do
            {
                cout << "\nLinkedList Menu:\n";
                cout << "1. Insert new flight\n";
                cout << "2. Delete Flight\n";
                cout << "3. Display All Flights\n";
                cout << "4. Back to Main Menu\n";
                cout << "Enter your choice: ";
                cin >> choice;

                switch (choice)
                {
                case 1:
                {
                    Flight f1(1, "AA4563", 600, "egypt airlines", "egypt", "6:00 am / nov. 16/11/2023", 4500.0);
                    Flight f2(2, "mk2286", 700, "egypt airlines", "egypt", "6:00 am / nov. 16/11/2023", 5500.0);
                    Flight f3(3, "sh1971", 800, "egypt airlines", "egypt", "6:00 am / nov. 16/11/2023", 7500.0); 


                    flightList.AddFlight(f1);
                    flightList.AddFlight(f2);
                    flightList.AddFlight(f3);
                    
                    break;
                }

                case 2:
                {
                    int id;
                    cout << "Enter flight id: " << endl;
                    cin >> id;
                    while (cin.fail())
                    {
                        cout << "Wrong input" << endl;
                        cin.clear();
                        cin.ignore();
                        cin >> id;
                    }
                    flightList.DelFlight(id);
                    break;
                }

                case 3:
                    flightList.DisplayAll();
                    break;

                case 4:
                    cout << "Returning to the Main Menu." << endl;
                    break;

                default:
                    cout << "Invalid choice. Please try again." << endl;
                    break;
                }

            } while (choice != 4);
        }
        break;

        case 2:
        {
            FlightStack<Flight> flightStack;

            int choice;

            do
            {
                cout << "\nStack Menu:\n";
                cout << "1. Insert new flight\n";
                cout << "2. Check the latest Added Flight\n";
                cout << "3. Print all the flights\n";
                cout << "4. Edit flight\n";
                cout << "5. Delete flight\n";
                cout << "6. Back to Main Menu\n";
                cout << "Enter your choice: ";
                cin >> choice;

                switch (choice)
                {
                case 1:
                {
                    Flight f1(1, "AA4563", 600, "egypt airlines", "egypt", "6:00 am / nov. 16/11/2023", 4500.0);
                    Flight f2(2, "mk2286", 700, "egypt airlines", "egypt", "6:00 am / nov. 16/11/2023", 5500.0);
                    Flight f3(3, "sh1971", 800, "egypt airlines", "egypt", "6:00 am / nov. 16/11/2023", 7500.0);   // Duplicate so will not be added
                    

                    flightStack.PushFlight(f1);
                    flightStack.PushFlight(f2);
                    flightStack.PushFlight(f3);
                    

                    break;
                }
                case 2:
                    flightStack.Peek();
                    break;

                case 3:
                    flightStack.PrintStack();
                    break;

                case 4:
                {
                    int id;
                    cout << "Enter flight id: " << endl;
                    cin >> id;
                    while (cin.fail())
                    {
                        cout << "Wrong input" << endl;
                        cin.clear();
                        cin.ignore();
                        cin >> id;
                    }
                    flightStack.EditStack(id);
                    break;
                }

                case 5:
                {
                    int id;
                    cout << "Enter flight id: " << endl;
                    cin >> id;
                    while (cin.fail())
                    {
                        cout << "Wrong input" << endl;
                        cin.clear();
                        cin.ignore();
                        cin >> id;
                    }
                    flightStack.DeleteStack(id);
                    break;
                }

                case 6:
                    cout << "Returning to the Main Menu." << endl;
                    break;

                default:
                    cout << "Invalid choice. Please try again." << endl;
                    break;
                }

            } while (choice != 6);
        };
        break;

        case 0:
            cout << "Exiting the program. Goodbye!" << endl;
            break;

        default:
            cout << "Invalid choice. Please try again." << endl;
            break;
        }

    } while (choice != 0);

    return 0;
}