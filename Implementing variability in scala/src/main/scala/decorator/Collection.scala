package de.uni_saarland.cs.se
package decorator


/**
 * Interface for the collection components and decorators
 *
 * @tparam A the type of elements in the collection
 */
trait Collection[A] {

  def push(element: A): Boolean

  def pop(): Option[A]

  def peek(): Option[A]

  def size: Int = 0
}

/**
 * Superclass for the concrete components.
 * @param ordering needed for the priority feature so that one can compare values in the collection;
 *                 To properly handle this parameter, subclasses should be declared as such:
 *                   class Foo[A : Ordering] extends AbstractCollection[A] {...}
 * @tparam A the type of elements in the collection
 */
abstract class AbstractCollection[A](implicit val ordering: Ordering[A]) extends Collection[A] {
  protected var elements: List[A] = Nil
  protected var head: Option[A] = None

  override def size(): Int = {
    elements.size
  }
}
class FIFOCollection[A](implicit order: Ordering[A]) extends AbstractCollection() {

  override def push(element: A): Boolean = {
    elements = element :: elements
    true
  }
  override def pop(): Option[A] = {
    if (elements == Nil) return None
    head = Some(elements.last)
    elements = elements.init
    head
  }
  override def peek(): Option[A] = {
    if (elements == Nil) return None
    head = Some(elements.last)
    head
  }
}

class LIFOCollection[A](implicit order: Ordering[A]) extends AbstractCollection() {
  override def push(element: A): Boolean = {
    elements = element :: elements
    true
  }
  override def pop(): Option[A] = {
    if (elements == Nil) return None
    head = Some(elements.reverse.last)
    elements = elements.reverse.init.reverse
    head
  }
  override def peek(): Option[A] = {
    if (elements == Nil) return None
    head = Some(elements.reverse.last)
    head
  }
}

class PriorityCollection[A](implicit order: Ordering[A]) extends AbstractCollection() {
  override def push(element: A): Boolean = {
    elements = element :: elements
    elements = elements.sorted
    println(elements)
    true
  }
  override def pop(): Option[A] = {
    if (elements == Nil) return None
    head = Some(elements.reverse.last)
    elements = elements.reverse.init.reverse
    head
  }
  override def peek(): Option[A] = {
    if (elements == Nil) return None
    head = Some(elements.reverse.last)
    head
  }
}

abstract class Decorator[A](access_type: Collection[A])(implicit  val ordering: Ordering[A])
  extends Collection[A] {

   override def push(element: A): Boolean = {
     access_type.push(element)
   }
  override def pop(): Option[A] = {
    access_type.pop()
  }
  override def peek(): Option[A] = {
    access_type.peek()
  }
  override def size(): Int = {
    access_type.size
  }
  def checkUniqueness(element: A): Boolean = {
    var el: List[A] = Nil

      for( a <- 1 to access_type.size){
        print(a)

        if (access_type.size > 0) {
          val p = access_type.pop().get
          el = p :: el
          access_type.push(p)
        }
      }
    if (el.contains(element)) true
    else false
  }

}


class CapacityDecorator[A](val capacity: Int, access_type: Collection[A])(implicit override val ordering: Ordering[A])
  extends Decorator(access_type){


  override def push(element: A): Boolean = {
    val x = super.size
    if (x >= capacity) false
    else super.push(element)
  }

  override def pop(): Option[A] = {
    super.pop()
  }

  override def peek(): Option[A] = {
    super.peek()
  }
  override def size(): Int = {
    super.size
  }

}

class UniquenessDecorator[A](access_type: Collection[A])(implicit override val ordering: Ordering[A])
  extends Decorator(access_type){

  override def push(element: A): Boolean = {
    if(super.checkUniqueness(element)) return false
    else super.push(element)
  }

  override def pop(): Option[A] = {
    super.pop()
  }

  override def peek(): Option[A] = {
    super.peek()
  }
  override def size(): Int = {
    super.size
  }
}

class LoggingDecorator[A](access_type: Collection[A])(implicit override val ordering: Ordering[A])
  extends Decorator(access_type){

  override def push(element: A): Boolean = {
    println(s"Pushing element $element.")
    super.push(element)
  }

  override def pop(): Option[A] = {
    if (super.size() == 0) {
      println("Collection is empty.")
      return None
    }
    else{
      val p = super.pop()
      println(s"Popping element ${p.get}.")
      p
    }
  }

  override def peek(): Option[A] = {
    if (super.size() == 0) {
      println("Collection is empty.")
      return None
    }
    val a = super.peek()
    println(s"Peeking element ${a.get}.")
    a
  }
  override def size(): Int = {
    val a = super.size
    println(s"Current size is ${a}.")
    a
  }

}
