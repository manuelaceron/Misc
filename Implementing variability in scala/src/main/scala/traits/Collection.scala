package de.uni_saarland.cs.se
package traits


/**
 * Interface for the collection implementations and traits
 *[A
 * Keep in mind that the priority feature needs an implicit parameter for the `Ordering` object:
 *   class Foo[A](implicit val ordering: Ordering[A]) extends Collection[A]
 *
 * @tparam A the type of elements in the collection
 */
trait Collection[A] {
  def push(element: A): Boolean

  def pop(): Option[A]

  def peek(): Option[A]

  def size: Int = 0
}

trait AbstractCollection[A] extends Collection[A] {
  var elements: List[A] = Nil
  var head: Option[A] = None

  override def push(element: A): Boolean = {
    var a: Boolean = false
    if (this.isInstanceOf[FIFOCollection[A]]) {
      a = this.push(element)
    }
    else if (this.isInstanceOf[LIFOCollection[A]]) {
      a = this.push(element)
    }
    else if (this.isInstanceOf[PriorityCollection[A]]) {
      a = this.push(element)
    }
    a
  }

  override def pop(): Option[A] = {
    var a : Option[A] = None
    if (this.isInstanceOf[FIFOCollection[A]]) {
      a = this.pop()
    }
    else if (this.isInstanceOf[LIFOCollection[A]]) {
      a = this.pop()
    }
    else if (this.isInstanceOf[PriorityCollection[A]]) {
      a = this.pop()
    }
    a
  }
  override def peek(): Option[A] = {
    var a : Option[A] = None
    if (this.isInstanceOf[FIFOCollection[A]]) {
      a = this.peek()
    }
    else if (this.isInstanceOf[LIFOCollection[A]]) {
      a = this.peek()
    }
    else if (this.isInstanceOf[PriorityCollection[A]]) {
      a = this.peek()
    }
    a
  }
}

class FIFOCollection[A] extends AbstractCollection[A] {

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
  override def size(): Int = {
    elements.size
  }
}

class LIFOCollection[A] extends AbstractCollection[A]{

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
  override def size(): Int = {
    elements.size
  }
}


class PriorityCollection[A](implicit order: Ordering[A]) extends AbstractCollection[A] {

  override def push(element: A): Boolean = {
    elements = element :: elements
    elements = elements.sorted
    true
  }
  override def pop(): Option[A] = {
    if (elements == Nil) return None
    head = Some(elements.reverse.last)
    elements = elements.reverse.init.reverse
    head
  }
  override def peek(): Option[A] = {
    if (elements == Nil) {
      return None
    }
    head = Some(elements.reverse.last)
    head
  }
  override def size(): Int = {
    val a = elements.size
    a
  }
}


trait Capacity[A] extends AbstractCollection[A]{
  val capacity: Int = 0

  override def push(element: A): Boolean = {
    if (elements.size >= capacity) return false
    super.push(element)
  }
}

trait Uniqueness[A] extends AbstractCollection[A]{
  override def push(element: A): Boolean = {
    if (elements.contains(element)) return false
    super.push(element)
  }
}

trait Logging[A] extends AbstractCollection[A]{

  override def push(element: A): Boolean = {
    val a = super.push(element)
    if(a) println(s"Pushing element $element.")
    else println("Failed to push element.")
    a
  }

  override def pop(): Option[A] = {
    val a = super.pop()
    if(!a.isEmpty) println(s"Popping element ${a.get}.")
    else println("Collection is empty.")
    a
  }

  override def peek(): Option[A] = {
    val a = super.peek()
    if(!a.isEmpty) println(s"Peeking element ${a.get}.")
    else println("Collection is empty.")
    a
  }
  override def size(): Int = {
    val a = elements.size
    println(s"Current size is ${a}.")
    a
  }
}