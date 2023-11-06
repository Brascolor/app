package com.brascolor.brascolor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping
public class BrascolorController {
    @Autowired
    private UserRepository userRepository;

    // Map ONLY POST Requests
    @PostMapping(path = "/add")
    public @ResponseBody User addNewUser(@RequestParam String name
            , @RequestParam String email) {
        // @ResponseBody means the returned User is the response, not a view name
        // @RequestParam means it is a parameter from the GET or POST request

        User springUser = new User();
        springUser.setName(name);
        springUser.setEmail(email);
        userRepository.save(springUser);
        return springUser;
    }

    @GetMapping(path = "/all")
    public @ResponseBody Iterable<User> getAllUsers() { 
        // This returns a JSON or XML with the users
        return userRepository.findAll();
    }
}
