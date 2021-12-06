package de.uni_saarland.cs.se
package runtime

abstract class CollectionAccess

case class FIFO() extends CollectionAccess

case class LIFO() extends CollectionAccess

case class PRIORITY() extends CollectionAccess


/**
 * Configuration object for the collection class.
 *
 * @param access the type of access to the collection
 * @param capacity the capacity of the collection or `None` for no capacity
 * @param uniqueness whether inserted elements need to be unique
 * @param logging whether to log function calls
 */
class CollectionConfig(
                        val access: CollectionAccess,
                        val capacity: Option[Int] = None,
                        val uniqueness: Boolean = false,
                        val logging: Boolean = false,
                      ) {}


/**
 * A runtime-configurable version of our collection SPL.
 *
 * @param config the configuration for the collection
 * @param ordering needed for the priority feature so that one can compare values in the collection
 * @tparam A the type of elements in the collection
 */
class Collection[A](val config: CollectionConfig)(implicit val ordering: Ordering[A]) {

  private var elements: List[A] = Nil
  private var head: Option[A] = None

  def push(element: A): Boolean = {
    if (!config.capacity.isEmpty){
      if (elements.size >= config.capacity.get){
        if (config.logging) println("Failed to push element.")
        return false
      }
    }
    if (config.uniqueness) {
      if(elements.contains(element)) {
        if (config.logging) println("Failed to push element.")
        return false
      }
    }

    if (config.logging) println(s"Pushing element $element.")

    if (config.access.isInstanceOf[FIFO] || config.access.isInstanceOf[LIFO] ) {
      elements = element :: elements
    }
    else if(config.access.isInstanceOf[PRIORITY] ){
      elements = element :: elements
      elements = elements.sorted
    }
    true
  }

  def pop(): Option[A] = {

    if (elements == Nil) {
      if (config.logging) println("Collection is empty.")
      return None
    }

    if (config.access.isInstanceOf[FIFO]){
      head = Some(elements.last)
      elements = elements.init
    }
    else if(config.access.isInstanceOf[LIFO] || config.access.isInstanceOf[PRIORITY]){
      head = Some(elements.reverse.last)
      elements = elements.reverse.init.reverse
    }

    if (config.logging) println(s"Popping element ${head.get}.")
    head
  }

  def size: Int = {
    if (config.logging) println(s"Current size is ${elements.size}.")
    elements.size
  }

  def peek(): Option[A] = {
    if (elements == Nil) {
      if (config.logging) println("Collection is empty.")
      return None
    }

    if (config.access.isInstanceOf[FIFO]){
      head = Some(elements.last)
    }
    else if(config.access.isInstanceOf[LIFO] || config.access.isInstanceOf[PRIORITY]){
      head = Some(elements.reverse.last)
    }

    if (config.logging) println(s"Peeking element ${head.get}.")
    head
  }

}
