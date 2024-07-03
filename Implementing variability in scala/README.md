# Implementing variability in Scala

Variability is crucial in Software Engineering. This Scala project addresses the need for flexible and dynamic collection management, ideal for applications requiring customizable behaviors like data structures, databases, or any system benefitting from adaptable collection operations. It enables runtime configuration of collection properties, supports feature enhancement through decorators, and facilitates flexible feature composition using traits and mixins, thereby promoting adaptability and maintainability in software development.

1. Runtime Parameters: Adjust collection behavior dynamically based on conditions during execution.
2. Decorator Pattern: Enhance collection functionality by dynamically wrapping objects.
3. Traits and Mixins: Compose collection behavior using Scala's traits, allowing flexible combination of features.

Testing is conducted using the AnyFlatSpec framework, ensuring thorough validation of application functionality.

## Runtime Parameters
This code implements a configurable collection framework, leveraging runtime parameters (given by a cofig) to determine collection behavior dynamically. Methods push, pop, peek, and size are used for manipulating elements based on access type (FIFO, LIFO, Priority), supporting features like capacity limits, uniqueness constraints, and function call logging. 

## Decorator Pattern
This code implements a collection framework using the decorator pattern. Decorators add dynamic features like capacity constraints, uniqueness checks, and logging to existing collection behaviors. Methods used include push, pop, peek, and size, offering flexible extension of collection functionality.

## Traits and Mixins
This code defines a collection framework using traits where concrete implementations and mixin traits provide configurable behaviors like FIFO, LIFO, priority handling, capacity constraints, uniqueness checks, and logging. Methods used include push, pop, peek, and size, enabling flexible composition and extension of collection features. 

