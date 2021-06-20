#ifndef LAB3_B_PLUS_HPP
#define LAB3_B_PLUS_HPP

#define SPACES 2
#define SEPARATORS 64

#include <vector>
#include <iostream>


namespace structures {

    template <typename T, typename K>
    class BPlusTree {

        public:

            explicit BPlusTree(int power) {
                root = nullptr;
                this->power = power;
            }

            void insert(K key, T value) {
                auto* element = new Element(key, value);

                if (root == nullptr) {
                    std::vector<Element> vector = {*element};
                    root = new Node(true, vector, {nullptr, nullptr});
                    return;
                }

                Node* toInsert = findLeaf(root, key);

                int pos = 0;

                while (pos < toInsert->elements.size() && toInsert->elements[pos].key < key) {
                    pos++;
                }

                auto it = toInsert->elements.begin() + pos;

                toInsert->elements.template emplace(it,  *element);
                toInsert->child.template emplace_back(nullptr);

                if (toInsert->elements.size() == power * 2) {
                    splitNode(toInsert);
                }
            }

            void erase(K key) {
                Node* toDelete = findLeaf(root, key);

                if (toDelete == root && toDelete->elements.size() == 1) {
                    root = nullptr;
                    return;
                }

                erase(toDelete, key);
            }

            T search(K key) {
                Node* toFind = findLeaf(root, key);

                int pos = 0;

                while (pos < toFind->elements.size() && toFind->elements[pos].key < key) {
                    pos++;
                }

                return toFind->elements[pos].value;
            }

            void output() {
                output(root, 0);
            }

        private:

            class Element {

            public:

                K key;
                T value;

                Element(K key, T value) {
                    this->key = key;
                    this->value = value;
                }
            };

            class Node {

            public:

                bool isLeaf{};
                std::vector<Element> elements;
                std::vector<Node*> child;
                Node* parent;
                Node* left_neighbor;
                Node* right_neighbor;

                Node(bool isLeaf, const std::vector<Element>& elements, const std::vector<Node*>& child) {
                    this->isLeaf = isLeaf;
                    this->elements = elements;
                    this->child = child;

                    parent = left_neighbor = right_neighbor = nullptr;
                }
            };

            int power{};

            Node* root;

            Node* findLeaf(Node* node, K toFind) {
                if (node->isLeaf) {
                    return node;
                }

                for (int i = 0; i < node->elements.size(); ++i) {
                    if (toFind < node->elements[i].key) {
                        return findLeaf(node->child[i], toFind);
                    }
                }

                return findLeaf(node->child[node->child.size() - 1], toFind);
            }

            void splitNode(Node* to_split) {
                std::vector<Node*> child_split;
                std::vector<Element> elements_split;

                Element middle = to_split->elements[power];

                for (int i = 0; i < power - 1; ++i) {
                    elements_split.template emplace_back(to_split->elements[i + power + 1]);
                    child_split.template emplace_back(to_split->child[i + power + 1]);
                }

                child_split.template emplace_back(to_split->child[power * 2]);

                if (to_split->isLeaf) {
                    elements_split.template emplace(elements_split.begin(), middle);
                    child_split.template emplace(child_split.begin(), nullptr);
                }

                Node* new_node = new Node(to_split->isLeaf, elements_split, child_split);

                for (int i = 0; i < power; ++i) {
                    to_split->elements.pop_back();
                    to_split->child.pop_back();
                }

                new_node->right_neighbor = to_split->right_neighbor;

                if (new_node->right_neighbor != nullptr) {
                    new_node->right_neighbor->left_neighbor = new_node;
                }

                to_split->right_neighbor = new_node;
                new_node->left_neighbor = to_split;

                if (to_split == this->root) {
                    this->root = new Node(false, {middle}, {to_split, new_node});

                    to_split->parent = root;
                    new_node->parent = root;
                }
                else {
                    Node* parent = to_split->parent;
                    new_node->parent = parent;

                    int pos = 0;

                    while (pos < parent->elements.size() && parent->elements[pos].key < middle.key) {
                        pos++;
                    }

                    auto first = parent->elements.begin() + pos;
                    parent->elements.template emplace(first, middle);

                    auto second = parent->child.begin() + pos + 1;
                    parent->child.template emplace(second, new_node);

                    if (parent->elements.size() == 2 * power) {
                        splitNode(parent);
                    }
                }
            }

            void erase(Node* to_delete, K key) {
                int pos = 0;

                while (pos < to_delete->elements.size() && to_delete->elements[pos].key < key) {
                    pos++;
                }

                if (to_delete == root && root->elements.size() == pos) {
                    root = root->child[0];
                    return;
                }

                to_delete->elements.erase(to_delete->elements.begin() + pos);
                to_delete->child.erase(to_delete->child.begin() + pos);

                if (to_delete->elements.size() >= power - 1) {
                    return;
                }

                Node* right = to_delete->right_neighbor;
                Node* left = to_delete->left_neighbor;

                if (left != nullptr && left->elements.size() > power - 1) {
                    to_delete->elements.template emplace(to_delete->elements.begin(),
                                                         left->elements[left->elements.size() - 1]);
                    to_delete->child.template emplace(to_delete->child.begin(),
                                                      left->child[left->child.size() - 1]);

                    left->elements.pop_back();
                    left->child.pop_back();

                    updateKeys(to_delete);
                }
                else if (right != nullptr && right->elements.size() > power - 1) {
                    to_delete->elements.template emplace_back(right->elements[0]);
                    to_delete->child.template emplace_back(right->child[0]);

                    right->elements.erase(right->elements.begin());
                    right->child.erase(right->child.begin());

                    updateKeys(to_delete);
                }
                else {
                    if (left != nullptr) {
                        for (int i = 0; i < to_delete->elements.size(); ++i) {
                            left->elements.template emplace_back(to_delete->elements[i]);
                            left->child.template emplace_back(to_delete->child[i]);
                        }

                        left->child.template emplace_back(to_delete->child[to_delete->child.size() - 1]);
                        left->right_neighbor = right;

                        if (right != nullptr) {
                            right->left_neighbor = left;
                        }

                        updateKeys(left);
                        erase(left->parent, to_delete->elements[0].key);

                    }
                    else if (right != nullptr) {
                        for (int i = 0; i < right->elements.size(); ++i) {
                            to_delete->elements.template emplace_back(right->elements[i]);
                            to_delete->child.template emplace_back(right->child[i]);
                        }

                        to_delete->child.template emplace_back(right->child[right->child.size() - 1]);
                        to_delete->right_neighbor = right->right_neighbor;

                        if (to_delete->right_neighbor != nullptr) {
                            to_delete->right_neighbor->left_neighbor = to_delete;
                        }

                        updateKeys(to_delete);

                        erase(to_delete->parent, right->elements[0].key);
                    }
                }

                if (root->elements.size() == 0) {
                    root = root->child[1];
                }
            }

            void updateKeys(Node* to_update) {
                if (to_update->parent == nullptr) {
                    return;
                }

                if (to_update->child.size() - to_update->elements.size() > 1 && !to_update->isLeaf) {
                    to_update->elements.clear();

                    for (int i = 1; i < to_update->child.size(); ++i) {
                        to_update->elements.template emplace_back(to_update->child[i]->elements[0]);
                    }
                }

                Node* parent = to_update->parent;

                int pos = 0;

                while (pos < parent->child.size() && parent->child[pos] != to_update) {
                    pos++;
                }

                if (pos > 0 && to_update->left_neighbor != nullptr) {
                    parent->elements[pos - 1] = to_update->elements[0];
                } else if (pos != parent->elements.size() && to_update->right_neighbor != nullptr &&
                           parent->elements[pos].key <= to_update->elements[to_update->elements.size() - 1].key) {
                    parent->elements[pos] = to_update->right_neighbor->elements[0];
                }

                updateKeys(parent);
            }

            void output(Node *node, int depth) const {
                if (!node) {
                    return;
                }

                if (node == this->root) {
                    std::cout << std::endl;

                    for (auto parent: node->elements) {
                        std::cout << parent.key << " ";
                    }

                    std::cout << std::endl;
                }
                else {
                    for (int space = 0; space < depth * SPACES; ++space) {
                        std::cout << " ";
                    }

                    for (auto child: node->elements) {
                        std::cout << child.key << " ";
                    }

                    std::cout << "[Parent=" << node->parent->elements[0].key << "]";
                    std::cout << std::endl;
                }

                if (node->isLeaf) {
                    return;
                }

                for (auto child: node->child) {
                    output(child, depth + 1);
                }
            }

    };
}

#endif
