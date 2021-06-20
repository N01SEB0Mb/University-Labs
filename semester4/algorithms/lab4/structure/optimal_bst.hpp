#ifndef LAB2_OPTIMAL_BST_HPP
#define LAB2_OPTIMAL_BST_HPP

#define SPACES 2
#define SEPARATORS 64

#include <cfloat>  // for double max value
#include <vector>
#include <iostream>


void print_separator(const std::string& text) {
    for (int separator = 0; separator < SEPARATORS; ++separator) {
        std::cout << "-";
    }

    std::cout << std::endl << text << std::endl;

    for (int separator = 0; separator < SEPARATORS; ++separator) {
        std::cout << "-";
    }

    std::cout << std::endl;
}


namespace structures {

    template<typename T>
    class OptimalBST {

        public:

            OptimalBST(const std::vector<T> &elements,
                       const std::vector<double> &probabilities,
                       const std::vector<double> &fict_probabilities) {
                int size = elements.size();

                this->root = nullptr;
                this->elements = elements;
                this->probabilities = probabilities;
                this->fict_probabilities = fict_probabilities;

                this->expected_values.assign(size + 2, {});
                this->probabilities_sum.assign(size + 2, {});
                this->roots.assign(size + 1, {});

                for (int i = 0; i < size + 2; ++i) {
                    expected_values[i].assign(size + 1, 0);
                    probabilities_sum[i].assign(size + 1, 0);
                }

                for (int i = 0; i < size + 1; ++i) {
                    roots[i].assign(size + 1, 0);
                }

                generateTables();

                // Output

                print_separator("Expected values:");

                for (auto &i: expected_values) {
                    for (auto &j: i) {
                        std::cout << j << "\t";
                    }

                    std::cout << std::endl;
                }

                print_separator("Probabilities sum:");

                for (auto &i: probabilities_sum) {
                    for (auto &j: i) {
                        std::cout << j << "\t";
                    }

                    std::cout << std::endl;
                }

                print_separator("Roots:");

                for (auto &i: roots) {
                    for (auto &j: i) {
                        std::cout << j << "\t";
                    }

                    std::cout << std::endl;
                }

                this->root = initializeBST(nullptr, 1, size);
            }

            ~OptimalBST() {
                for (int i = 0; i < elements.size() + 2; ++i) {
                    expected_values[i].clear();
                    probabilities_sum[i].clear();
                }

                for (int i = 0; i < elements.size() + 1; ++i) {
                    roots[i].clear();
                }

                expected_values.clear();
                probabilities_sum.clear();
                roots.clear();

                destroy(this->root);

                std::cout << "Tree destroyed" << std::endl;
            }

            void output() {
                output(this->root, 0, true);
            }

        private:

            class Node {

            public:

                T value;
                Node *parent;
                Node *left;
                Node *right;
                double probability{};

                Node() {
                    left = right = parent = nullptr;
                    probability = 0;
                }

                Node(const T &value, double probability) {
                    this->value = value;
                    left = right = parent = nullptr;
                    this->probability = probability;
                }

                ~Node() = default;
            };

            Node *root;

            std::vector<T> elements;
            std::vector<double> probabilities;
            std::vector<double> fict_probabilities;

            std::vector<std::vector<double>> expected_values;
            std::vector<std::vector<double>> probabilities_sum;
            std::vector<std::vector<int>> roots;

            void generateTables() {
                int size = elements.size();

                for (int i = 1; i < size + 2; ++i) {
                    expected_values[i][i - 1] = fict_probabilities[i - 1];
                    probabilities_sum[i][i - 1] = fict_probabilities[i - 1];
                }

                int j;
                double t;

                print_separator("Generating tables:");

                for (int l = 1; l < size + 1; ++l) {
                    for (int i = 1; i < size - l + 2; ++i) {
                        j = i + l - 1;

                        expected_values[i][j] = DBL_MAX;
                        probabilities_sum[i][j] = probabilities_sum[i][j - 1] + probabilities[j - 1] + fict_probabilities[j];

                        for (int r = i; r < j + 1; ++r) {
                            t = expected_values[i][r - 1] + expected_values[r + 1][j] + probabilities_sum[i][j];

                            std::cout << t << "\t";

                            if (t < expected_values[i][j]) {
                                expected_values[i][j] = t;
                                roots[i][j] = r;
                            }
                        }
                    }
                }

                std::cout << std::endl;
            }

            Node *initializeBST(Node *node, int low, int high) {
                if (low > high) {
                    return new Node(T(), fict_probabilities[high]);
                }

                int current_index = roots[low][high] - 1;
                Node *temp_root = new Node(elements[current_index], probabilities[current_index]);

                temp_root->left = initializeBST(temp_root, low, roots[low][high] - 1);
                temp_root->right = initializeBST(temp_root, roots[low][high] + 1, high);
                temp_root->parent = node;

                return temp_root;
            }

            void destroy(Node *to_destroy) {
                if (!to_destroy)
                    return;

                destroy(to_destroy->left);
                destroy(to_destroy->right);

                delete to_destroy;
            }

            void output(Node *node, int depth, bool is_left) const {
                if (!node) {
                    return;
                }

                for (int space = 0; space < depth * SPACES; ++space) {
                    std::cout << " ";
                }

                if (node == this->root) {
                    std::cout << node->value;
                    std::cout << " (Parent)";
                    std::cout << " <Probability=" << node->probability << ">";
                    std::cout << std::endl;
                }
                else {
                    std::cout << node->value;
                    std::cout << (is_left ? " (L)" : " (R)");
                    std::cout << " <Probability=" << node->probability << ">";
                    std::cout << std::endl;
                }

                output(node->left, depth + 1, true);
                output(node->right, depth + 1, false);
            }

    };

}  // namespace structures

#endif
