#include <iostream>
#include <cstring>
using namespace std;

void secret_function() {
    cout << "\n!!! YOU SHOULD NOT BE HERE !!!\n";
    cout << "Access granted → secret data unlocked.\n";
    cout << "Flag: STACK_OVERFLOW_{classic_classic_vuln}\n\n";
}

void vulnerable_function(const char* user_input) {
    char buffer[32];           // ← small buffer

    cout << "buffer is at: " << (void*)buffer << "\n";

    // Classic dangerous copy — no bounds checking
    strcpy(buffer, user_input);

    cout << "You said: " << buffer << "\n";
}

int main() {
    char name[200];   // much larger than the destination buffer

    cout << "What's your name? ";
    // cin >> name;                   // safe version (but boring)
    cin.getline(name, sizeof(name));   // allows spaces, still dangerous when passed

    cout << "\nTrying to say hello...\n";
    vulnerable_function(name);

    cout << "\nBack in main — everything seems fine?\n";

    return 0;
}
