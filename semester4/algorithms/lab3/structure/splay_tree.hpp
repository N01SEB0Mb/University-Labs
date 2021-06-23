#ifndef LAB3_SPLAY_TREE_HPP
#define LAB3_SPLAY_TREE_HPP

#define SPACES 2
#define P 101
#define Q 3571

#include <cmath>
#include <iostream>


namespace structures {

    template <typename T>
    class SplayTree {

    public:

        SplayTree() {
            this->root = nullptr;
        }
        ~SplayTree() = default;

        void insert(std::string &name) {
            if (!this->root) {
                this->root = new Node(name);
                return;
            }
            else {
                split(name);
            }
        }

        void erase(std::string &name) {
            Node* to_delete = erase(this->root, name);

            std::cout << to_delete->name << std::endl;

            splay(to_delete, this->root);
            merge(this->root->left, this->root->right);

            if (this->root) {
                this->root->parent = nullptr;
            }
        }

        std::string get(std::string &name) {
            Node* res = get(this->root, name);

            if (res) {
                splay(res, this->root);
                return res->name;
            }
            else {
                return std::string();
            }
        }

        void output() {
            output(this->root, 0, true);
        }

    private:

        class Node {

        public:

            T value;
            std::string name;

            Node* parent;
            Node* left;
            Node* right;

            explicit Node(std::string &name) {
                this->name = name;
                this->value = hash(name);

                left = right = parent = nullptr;
            }

        private:

            T hash(std::string &string) {
                T result = 0;

                for (char c: string) {
                    if (c != ' ') {
                        result = (P * result + tolower(c)) % Q;
                    }
                }

                return result;
            }
        };

        Node* root;

        void splay(Node* to_splay, Node* root_splay) {
            std::cout << std::endl;
            std::cout << "To splay:   " << to_splay->name << std::endl;
            std::cout << "Root splay: " << root_splay->name << std::endl;

            Node* parent = root_splay->parent;

            while (to_splay->parent && to_splay->parent != parent) {
                // Check if parent has parent

                if (!to_splay->parent->parent) {
                    // Zig (rotate on the edge between current and parent)

                    zig(to_splay, to_splay == to_splay->parent->left);
                }
                else {
                    if ((to_splay == to_splay->parent->left) ==
                        (to_splay->parent == to_splay->parent->parent->left)) {
                        // Zig-Zig (rotate on the edge joining parent)

                        zig_zig(to_splay, to_splay == to_splay->parent->left);
                    }
                    else {
                        // Zig-Zag (rotate on the edge, then rotate on the resulting edge)

                        zig_zag(to_splay, to_splay->parent == to_splay->parent->parent->left);
                    }
                }
            }

            if (parent == nullptr) {
                this->root = to_splay;
            }
        }

        void zig(Node* to_splay, bool is_left) {
            std::cout << "> Zig step" << std::endl;

            Node* parent = to_splay->parent;

            if (is_left) {
                parent->left = to_splay->right;

                if (to_splay->right != nullptr) {
                    parent->left->parent = parent;
                }

                to_splay->right = parent;
            }
            else {
                parent->right = to_splay->left;

                if (to_splay->left != nullptr) {
                    parent->right->parent = parent;
                }

                to_splay->left = parent;
            }

            to_splay->parent = parent->parent;

            if (to_splay->parent != nullptr) {
                if (parent == to_splay->parent->left) {
                    to_splay->parent->left = to_splay;
                }
                else {
                    to_splay->parent->right = to_splay;
                }
            }

            parent->parent = to_splay;
        }

        void zig_zig(Node* to_splay, bool is_left) {
            std::cout<< "> Zig-Zig step" << std::endl;

            Node* parent = to_splay->parent;
            Node* gran = parent->parent;

            if (is_left) {
                gran->left = parent->right;

                if (parent->right != nullptr) {
                    gran->left->parent = gran;
                }

                parent->left = to_splay->right;

                if (to_splay->right != nullptr) {
                    parent->left->parent = parent;
                }

                parent->right = gran;
                to_splay->right = parent;
            }
            else {
                gran->right = parent->left;

                if (parent->left != nullptr) {
                    gran->right->parent = gran;
                }

                parent->right = to_splay->left;

                if (to_splay->left != nullptr) {
                    parent->right->parent = parent;
                }

                parent->left = gran;
                to_splay->left = parent;
            }

            to_splay->parent = gran->parent;

            if (gran->parent != nullptr) {
                if (gran == gran->parent->left) {
                    gran->parent->left = to_splay;
                }
                else {
                    gran->parent->right = to_splay;
                }
            }

            gran->parent = parent;
            parent->parent = to_splay;
        }

        void zig_zag(Node* to_splay, bool is_left) {
            std::cout<< "> Zig-Zag step" << std::endl;

            Node* parent = to_splay->parent;
            Node* gran = parent->parent;

            if (is_left) {
                parent->right = to_splay->left;

                if (to_splay->left != nullptr) {
                    parent->right->parent = parent;
                }

                gran->left = to_splay->right;

                if (to_splay->right != nullptr) {
                    gran->left->parent = gran;
                }

                to_splay->left = parent;
                to_splay->right = gran;
                parent->parent = to_splay;
            }
            else {
                parent->left = to_splay->right;

                if (to_splay->right != nullptr) {
                    parent->left->parent = parent;
                }

                gran->right = to_splay->left;

                if (to_splay->left != nullptr) {
                    gran->right->parent = gran;
                }

                to_splay->right = parent;
                to_splay->left = gran;
                parent->parent = to_splay;
            }

            to_splay->parent = gran->parent;

            if (gran->parent != nullptr) {
                if (gran == gran->parent->left) {
                    gran->parent->left = to_splay;
                }
                else {
                    gran->parent->right = to_splay;
                }
            }

            gran->parent = to_splay;
            parent->parent = to_splay;
        }

        Node* erase(Node* node, std::string &name) {
            if (node == nullptr) {
                return nullptr;
            }

            Node* temp = new Node(name);

            if (temp->value < node->value) {
                return erase(node->left, name);
            }
            else if (temp->value > node->value) {
                return erase(node->right, name);
            }
            else {
                return node;
            }
        }

        Node* get(Node* node, std::string &name) {
            if (!node) {
                return nullptr;
            }

            if (Node(name).value < node->value) {
                return get(node->left, name);
            }
            else if (Node(name).value > node->value) {
                return get(node->right, name);
            }
            else {
                return node;
            }
        }

        void merge(Node* root_left, Node* root_right) {
            // Check if left or right roots are nullptr

            if (!root_left || !root_right) {
                this->root = !root_left ? root_right : root_left;
                return;
            }

            Node* max_left = root_left->right;

            if (!max_left) {
                root_left->right = root_right;
                root_right->parent = root_left;

                this->root = root_left;

                return;
            }

            while (max_left->right) {
                max_left = max_left->right;
            }

            splay(max_left, root_left);

            max_left->right = root_right;
            root_right->parent = max_left;

            this->root = max_left;
        }

        void split(std::string &name) {
            Node* successor;
            Node* temp = this->root;
            Node* to_insert = new Node(name);

            while (temp) {
                if (temp->value < to_insert->value) {
                    successor = temp;
                    temp = temp->right;
                }
                else if (temp->value > to_insert->value) {
                    successor = temp;
                    temp = temp->left;
                }
                else {
                    successor = temp;
                    temp = nullptr;
                }
            }

            splay(successor, this->root);

            if (successor->value < to_insert->value) {
                to_insert->left = successor;
            }
            else {
                to_insert->left = successor->left;

                if (to_insert->left != nullptr) {
                    to_insert->left->parent = to_insert;
                }

                successor->left = nullptr;
                to_insert->right = successor;
            }

            successor->parent = to_insert;
            this->root = to_insert;
        }

        void output(Node* node, int depth, bool is_left) const {
            if (!node) {
                return;
            }

            for (int space = 0; space < depth * SPACES; ++space) {
                std::cout << " ";
            }

            if (node == this->root) {
                std::cout << std::endl;
                std::cout << node->name;
                std::cout << " (Parent)" << std::endl;
            }
            else {
                std::cout << node->name;
                std::cout << (is_left ? " (L) " : " (R) ");
                // std::cout << "[Parent=" << node->parent->value << "]";
                std::cout << std::endl;
            }

            output(node->left, depth + 1, true);
            output(node->right, depth + 1, false);
        }

    };

} // namespace structures

#endif
