The endpoint can be `GET /people/<person_id>/connections_of_degree?degree=<degree>`. I would implement it as follows (in pseudo-Python-code) in the `Person` model class:

    def connections_separated_by_degrees(self, degree):
        all_connections = {}
        current_connections = self.connections
        while degree > 0:
            all_connections |= current_connections
            new_current_connections = {}
            for connection in current_connections:
                new_current_connections |= connection.connections
            current_connections = new_current_connections
            degree =- 1
        return all_connections

Of course, this method can be implemented to be recursive, instead of iterative (which it currently is). The recursive version would be as follows:

    def connections_separated_by_degrees(self, degree):
        if degree < 1:
            return {}
        else:
            all_connections = {}
            for connection in self.connections:
                all_connections |= connections_separated_by_degrees(connection, degree - 1)
            return all_connections

A potential challenge is the performance. If the people have a lot of connections, and/or if the the degree of separation is a big number, the function can take a serious time running. In such case, an out of memory error can occur. Or the recursive version might cause a stack overflow error.

One potential question that I would ask to PO is if we want to retain the degree of separation for each connection in the result. That is, currently this code will return all connections that are by `degree` degrees apart, but we won't be able to tell exactly how many degrees away a given connection is from the original connection. If we want to retain this information as well, there must be a change in the implementation.
